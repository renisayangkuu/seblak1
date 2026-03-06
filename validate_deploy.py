"""
Script untuk validasi kesiapan deployment ke Railway
"""
import os
import sys

def validate_deployment():
    """Validate all required files for Railway deployment"""
    
    print("🔍 Validating Railway deployment readiness...\n")
    
    required_files = {
        'bot.py': 'Main bot file',
        'requirements.txt': 'Python dependencies',
        'runtime.txt': 'Python version',
        'Procfile': 'Process type',
        'railway.json': 'Railway config',
        'nixpacks.toml': 'Build config',
        '.railwayignore': 'Ignore file',
        'init_railway.py': 'Database initializer',
        'seed_menu.py': 'Menu seeder',
        '.env.example': 'Environment template',
        '.gitignore': 'Git ignore',
        'README.md': 'Documentation',
        'DEPLOYMENT.md': 'Deploy guide',
    }
    
    optional_files = {
        'CHECKLIST_DEPLOY.md': 'Deploy checklist',
    }
    
    errors = []
    warnings = []
    success = []
    
    # Check required files
    print("📋 Checking required files:")
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {description}")
            success.append(file)
        else:
            print(f"  ❌ {file} - {description} (MISSING!)")
            errors.append(file)
    
    print()
    
    # Check optional files
    print("📋 Checking optional files:")
    for file, description in optional_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {description}")
        else:
            print(f"  ⚠️  {file} - {description} (optional)")
            warnings.append(file)
    
    print()
    
    # Check gambar folder
    print("📋 Checking gambar folder:")
    if os.path.exists('gambar'):
        images = [f for f in os.listdir('gambar') 
                 if f.endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp'))]
        if len(images) >= 3:
            print(f"  ✅ gambar/ folder exists with {len(images)} images")
            print(f"     Images: {', '.join(images[:3])}")
        else:
            print(f"  ⚠️  gambar/ folder exists but only has {len(images)} images")
            print(f"     Need at least 3 images for menu")
            warnings.append('gambar/ (insufficient images)')
    else:
        print(f"  ❌ gambar/ folder not found")
        errors.append('gambar/')
    
    print()
    
    # Check .env.example
    print("📋 Checking .env.example:")
    if os.path.exists('.env.example'):
        with open('.env.example', 'r', encoding='utf-8') as f:
            content = f.read()
            required_vars = [
                'TELEGRAM_BOT_TOKEN',
                'ADMIN_TELEGRAM_IDS',
                'ADMIN_PASSWORD',
                'WARUNG_NAME',
                'BANK_NAME',
                'BANK_ACCOUNT',
            ]
            missing_vars = [var for var in required_vars if var not in content]
            if missing_vars:
                print(f"  ⚠️  Missing variables: {', '.join(missing_vars)}")
                warnings.append('.env.example (missing variables)')
            else:
                print(f"  ✅ All required variables present")
    
    print()
    
    # Check if .env exists (should NOT be pushed)
    print("📋 Checking .gitignore:")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            content = f.read()
            if '.env' in content and '*.db' in content:
                print(f"  ✅ .gitignore properly configured")
            else:
                print(f"  ⚠️  .gitignore might be missing important entries")
                warnings.append('.gitignore (check entries)')
    
    print()
    print("=" * 60)
    print()
    
    # Summary
    if errors:
        print(f"❌ VALIDATION FAILED!")
        print(f"\n🚫 Missing required files ({len(errors)}):")
        for error in errors:
            print(f"   - {error}")
        print(f"\n⚠️  Please create missing files before deploying!")
        return False
    elif warnings:
        print(f"⚠️  VALIDATION PASSED WITH WARNINGS")
        print(f"\n✅ All required files present ({len(success)})")
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"   - {warning}")
        print(f"\n💡 You can proceed with deployment, but consider fixing warnings.")
        return True
    else:
        print(f"✅ VALIDATION PASSED!")
        print(f"\n🎉 All files ready for Railway deployment!")
        print(f"\n📝 Next steps:")
        print(f"   1. Push to GitHub: git add . && git commit -m 'Ready for deploy' && git push")
        print(f"   2. Create project on Railway.app")
        print(f"   3. Set environment variables")
        print(f"   4. Deploy!")
        print(f"\n📖 See DEPLOYMENT.md for detailed instructions")
        return True

if __name__ == "__main__":
    success = validate_deployment()
    sys.exit(0 if success else 1)
