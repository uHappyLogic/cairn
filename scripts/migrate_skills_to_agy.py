import os
import re
import shutil
import json
import sys

# `${CLAUDE_PLUGIN_ROOT}` is a Claude Code runtime variable that Antigravity does not
# define, so every reference to it is rewritten at generation time into a path relative to
# the workspace root, where the generated plugin tree lives.
PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"

# The prose hint that tells a Claude Code runner it can resolve the variable with a shell
# echo. Once the path is literal the hint is meaningless, so it is dropped along with the
# whitespace in front of it (the sentence it sits in wraps, so the spacing varies).
RESOLVE_HINT_RE = re.compile(
    r'\s*\(run\s+`echo\s+"\$CLAUDE_PLUGIN_ROOT"`\s+if\s+you\s+need\s+to\s+resolve\s+the\s+path\)'
)


def rewrite_plugin_root(content, plugin_dir):
    """Rewrite plugin-root references into paths that resolve in the generated tree."""
    content = RESOLVE_HINT_RE.sub("", content)
    return content.replace(PLUGIN_ROOT_VAR, plugin_dir.replace(os.sep, "/"))


def rewrite_tree(dest_dir, plugin_dir):
    """Apply rewrite_plugin_root to every text file already copied under dest_dir."""
    for root, _dirs, files in os.walk(dest_dir):
        for name in files:
            path = os.path.join(root, name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            rewritten = rewrite_plugin_root(content, plugin_dir)
            if rewritten != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(rewritten)


def read_source_version(src_manifest):
    """Read the plugin version from the source Claude Code manifest.

    That manifest is the single source of truth for the version, so the generated
    Antigravity manifest is correct on every regeneration path without the version
    script ever writing it.
    """
    if not os.path.exists(src_manifest):
        print(f"Error: source manifest {src_manifest} not found (run this script from the repository root)", file=sys.stderr)
        sys.exit(1)

    try:
        with open(src_manifest, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: could not read source manifest {src_manifest}: {e}", file=sys.stderr)
        sys.exit(1)

    version = data.get("version")
    if not isinstance(version, str) or not version:
        print(f"Error: source manifest {src_manifest} has no 'version' value to copy", file=sys.stderr)
        sys.exit(1)

    return version


def migrate_to_agy_plugin(plugin_name="cairn", src_skills="skills", src_agents="agents", src_shared="shared", src_mcp=".mcp.json", src_manifest=os.path.join(".claude-plugin", "plugin.json")):
    plugin_dir = os.path.join(".agents", "plugins", plugin_name)

    print(f"Creating agy plugin '{plugin_name}' at '{plugin_dir}'...")
    os.makedirs(plugin_dir, exist_ok=True)

    # 1. Create plugin.json
    version = read_source_version(src_manifest)
    manifest_path = os.path.join(plugin_dir, "plugin.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump({
            "$schema": "https://antigravity.google/schemas/v1/plugin.json",
            "name": plugin_name,
            "description": f"Ported plugin for {plugin_name}",
            "version": version
        }, f, indent=2)
    print(f"Created manifest at {manifest_path} with version {version}")

    # 2. Migrate MCP config
    if os.path.exists(src_mcp):
        dest_mcp = os.path.join(plugin_dir, "mcp_config.json")
        try:
            with open(src_mcp, 'r', encoding='utf-8') as f:
                mcp_data = json.load(f)
                
            if "mcpServers" not in mcp_data:
                print("Warning: Source MCP file does not contain 'mcpServers'. Proceeding anyway.")
                
            with open(dest_mcp, 'w', encoding='utf-8') as f:
                json.dump(mcp_data, f, indent=2)
                
            print(f"Successfully migrated MCP config to {dest_mcp}")
        except Exception as e:
            print(f"Error migrating MCP config: {e}")
    else:
        print(f"No source MCP config found at {src_mcp}")

    # 3. Migrate skills
    if os.path.exists(src_skills):
        dest_skills_dir = os.path.join(plugin_dir, "skills")
        if os.path.exists(dest_skills_dir):
            shutil.rmtree(dest_skills_dir)
        os.makedirs(dest_skills_dir, exist_ok=True)
        
        count = 0
        for skill_name in os.listdir(src_skills):
            src_skill_path = os.path.join(src_skills, skill_name)
            if not os.path.isdir(src_skill_path):
                continue
                
            if skill_name.endswith("-workspace"):
                continue
                
            skill_md_path = os.path.join(src_skill_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                # Create a directory for this skill
                dest_skill_dir = os.path.join(dest_skills_dir, skill_name)
                os.makedirs(dest_skill_dir, exist_ok=True)
                dest_skill_md_path = os.path.join(dest_skill_dir, "SKILL.md")
                
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                import yaml
                if not content.startswith('---'):
                    print(f"Error: {skill_name} is missing YAML frontmatter in SKILL.md", file=sys.stderr)
                    sys.exit(1)
                
                parts = content.split('---', 2)
                if len(parts) == 3:
                    frontmatter_str = parts[1]
                    try:
                        fm = yaml.safe_load(frontmatter_str)
                    except yaml.YAMLError:
                        lines = frontmatter_str.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith('description: '):
                                desc = line[len('description: '):].strip()
                                if not desc.startswith('"') and not desc.startswith("'"):
                                    desc = desc.replace('"', '\\"')
                                    lines[i] = f'description: "{desc}"'
                        new_fm = '\n'.join(lines)
                        content = f"---{new_fm}---{parts[2]}"
                        try:
                            fm = yaml.safe_load(new_fm)
                        except yaml.YAMLError:
                            print(f"Error: {skill_name} has invalid YAML frontmatter in SKILL.md", file=sys.stderr)
                            sys.exit(1)
                    
                    if not fm or 'name' not in fm or 'description' not in fm:
                        print(f"Error: {skill_name} is missing 'name' or 'description' in YAML frontmatter in SKILL.md", file=sys.stderr)
                        sys.exit(1)
                else:
                    print(f"Error: {skill_name} has malformed YAML frontmatter in SKILL.md", file=sys.stderr)
                    sys.exit(1)
                    
                with open(dest_skill_md_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                # Copy any other files in the skill directory to the new skill directory
                for item in os.listdir(src_skill_path):
                    if item == "SKILL.md":
                        continue
                    s = os.path.join(src_skill_path, item)
                    d = os.path.join(dest_skill_dir, item)
                    
                    if os.path.isdir(s):
                        if not os.path.exists(d):
                            shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
                        
                print(f"Successfully migrated skill: {skill_name} to {dest_skill_md_path}")
                count += 1
            else:
                print(f"Warning: No SKILL.md found in {skill_name}")

        rewrite_tree(dest_skills_dir, plugin_dir)
        print(f"Successfully migrated {count} skills to {dest_skills_dir}")
    else:
        print(f"No source skills found at {src_skills}")

    # 4. Migrate agents
    if os.path.exists(src_agents):
        dest_agents_dir = os.path.join(plugin_dir, "agents")
        if os.path.exists(dest_agents_dir):
            shutil.rmtree(dest_agents_dir)
        shutil.copytree(src_agents, dest_agents_dir)
        rewrite_tree(dest_agents_dir, plugin_dir)
        print(f"Successfully migrated agents to {dest_agents_dir}")
    else:
        print(f"No source agents found at {src_agents}")

    # 5. Migrate shared procedures
    if os.path.exists(src_shared):
        dest_shared_dir = os.path.join(plugin_dir, "shared")
        if os.path.exists(dest_shared_dir):
            shutil.rmtree(dest_shared_dir)
        shutil.copytree(src_shared, dest_shared_dir)
        rewrite_tree(dest_shared_dir, plugin_dir)
        print(f"Successfully migrated shared procedures to {dest_shared_dir}")
    else:
        print(f"No source shared procedures found at {src_shared}")

if __name__ == "__main__":
    migrate_to_agy_plugin()
