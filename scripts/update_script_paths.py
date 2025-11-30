import os

def update_workflow_paths():
    # We need to update .github/workflows/lint.yml if it references scripts/scraper
    # Also check scraper.service or setup_ubuntu.sh if they hardcode paths
    
    # Update setup_ubuntu.sh
    setup_path = 'scripts/scrapers/content_scraper/setup_ubuntu.sh'
    if os.path.exists(setup_path):
        with open(setup_path, 'r') as f:
            content = f.read()
        
        # Update systemd service path
        content = content.replace('scripts/scraper/scraper.service', 'scripts/scrapers/content_scraper/scraper.service')
        # Update working directory in general logic if any
        
        with open(setup_path, 'w') as f:
            f.write(content)
        print(f"Updated {setup_path}")

    # Update scraper.service
    service_path = 'scripts/scrapers/content_scraper/scraper.service'
    if os.path.exists(service_path):
        with open(service_path, 'r') as f:
            content = f.read()
        
        # Update paths in service file
        # WorkingDirectory=/opt/Hong-Kong-Fire-Documentary/scripts/scraper
        content = content.replace('/scripts/scraper', '/scripts/scrapers/content_scraper')
        # ExecStart=/opt/Hong-Kong-Fire-Documentary/scripts/scraper/daemon.py
        content = content.replace('/scripts/scraper/daemon.py', '/scripts/scrapers/content_scraper/daemon.py')
        
        with open(service_path, 'w') as f:
            f.write(content)
        print(f"Updated {service_path}")

if __name__ == "__main__":
    update_workflow_paths()

