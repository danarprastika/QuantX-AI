const fs = require('fs');
const path = require('path');

function checkErrorBoundaries() {
  const pagesDir = path.join(__dirname, '../src/presentation/pages');
  const componentsDir = path.join(__dirname, '../src/presentation/components');
  
  let hasErrors = false;
  const routes = [];

  function findPageFiles(dir) {
    const files = fs.readdirSync(dir);
    files.forEach((file) => {
      const filePath = path.join(dir, file);
      if (fs.statSync(filePath).isDirectory()) {
        findPageFiles(filePath);
      } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
        routes.push(filePath);
      }
    });
  }

  findPageFiles(pagesDir);

  routes.forEach((routePath) => {
    const content = fs.readFileSync(routePath, 'utf8');
    const routeName = routePath.split('pages')[1];
    
    const hasErrorBoundary = content.includes('ErrorBoundary') || 
                            routePath.includes('error') ||
                            fs.existsSync(path.join(path.dirname(routePath), 'error.tsx'));
    
    if (!hasErrorBoundary) {
      console.warn(`Warning: Route ${routeName} may need ErrorBoundary wrapper`);
    }
  });

  if (fs.existsSync(componentsDir)) {
    const commonDir = path.join(componentsDir, 'common');
    if (!fs.existsSync(commonDir)) {
      console.error('Error: Missing common components directory');
      hasErrors = true;
    }
  }

  if (hasErrors) {
    console.error('\nError boundary check failed');
    process.exit(1);
  }
  
  console.log('Error boundary check passed');
}

checkErrorBoundaries();