import argparse
import os
from pathlib import Path

def scaffold(project_name, host_port, description, use_llm):
    project_name_hyphenated = project_name.replace("_", "-")
    project_name_pretty = project_name.replace("_", " ").title()
    
    # Define paths
    base_dir = Path.cwd()
    template_dir = Path(__file__).parent.parent / "resources" / "templates"
    src_dir = base_dir / "src" / project_name
    test_dir = base_dir / "tests"
    
    # Helper to replace placeholders
    def render(content):
        replacements = {
            "{{ project_name }}": project_name,
            "{{ project_name_hyphenated }}": project_name_hyphenated,
            "{{ project_name_pretty }}": project_name_pretty,
            "{{ host_port }}": str(host_port),
            "{{ description }}": description,
            "{{ author_name }}": "genwch",
            "{{ author_email }}": "geo.wong@gmail.com",
        }
        # Simple conditional logic for templates
        if use_llm:
            content = content.replace("{% if use_llm %}", "").replace("{% endif %}", "")
        else:
            import re
            content = re.sub(r"{% if use_llm %}.*?{% endif %}", "", content, flags=re.DOTALL)
            
        for key, value in replacements.items():
            content = content.replace(key, value)
        return content

    # Create directories
    src_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / "data").mkdir(exist_ok=True)
    (base_dir / "scripts").mkdir(exist_ok=True)

    # Files to process (template_name, target_path)
    files = [
        ("Dockerfile.template", base_dir / "Dockerfile"),
        ("docker-compose.yml.template", base_dir / "docker-compose.yml"),
        ("pyproject.toml.template", base_dir / "pyproject.toml"),
        ("env.sample.template", base_dir / ".env.sample"),
        ("README.md.template", base_dir / "README.md"),
        ("main.py.template", src_dir / "main.py"),
        ("pre_deploy_check.sh.template", base_dir / "scripts" / "pre_deploy_check.sh"),
        ("test_main.py.template", test_dir / "test_main.py"),
    ]

    for template_name, target_path in files:
        template_file = template_dir / template_name
        if template_file.exists():
            content = template_file.read_text()
            target_path.write_text(render(content))
            print(f"Created {target_path}")

    # Create empty __init__.py files
    (src_dir / "__init__.py").touch()
    (base_dir / "src" / "__init__.py").touch()

    # Make scripts executable
    os.chmod(base_dir / "scripts" / "pre_deploy_check.sh", 0o755)

    print(f"\nProject {project_name} scaffolded successfully!")
    print(f"1. Run 'uv sync'")
    print(f"2. Copy .env.sample to .env and adjust values")
    print(f"3. Run 'scripts/pre_deploy_check.sh' to verify baseline")
    print(f"4. Run 'podman-compose up -d'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new Homelab project.")
    parser.add_argument("name", help="Project name (use underscores, e.g., my_new_app)")
    parser.add_argument("--port", type=int, required=True, help="Host port mapping (> 20000)")
    parser.add_argument("--description", default="A new homelab project", help="Project description")
    parser.add_argument("--llm", action="store_true", help="Include LLM integration patterns")
    
    args = parser.parse_args()
    
    if args.port <= 20000:
        print("Error: Port must be greater than 20000.")
        exit(1)
        
    scaffold(args.name, args.port, args.description, args.llm)
