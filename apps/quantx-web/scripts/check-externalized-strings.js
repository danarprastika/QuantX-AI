const fs = require('fs');
const path = require('path');

function checkExternalizedStrings() {
  const srcDir = path.join(__dirname, '../src');
  let hardcodedCount = 0;

  function checkFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    
    const stringMatches = content.match(/['"`]([A-Z][^'"`]*[a-z][^'"`]*)['"`]/g);
    
    if (stringMatches) {
      const nonI18nStrings = stringMatches.filter((match) => {
        const cleaned = match.slice(1, -1);
        return !cleaned.includes('{{') && 
               cleaned.length > 10 && 
               !filePath.includes('test') &&
               !filePath.includes('.json');
      });
      
      if (nonI18nStrings.length > 0) {
        console.warn(`Warning: Potential hardcoded strings in ${filePath}: ${nonI18nStrings.length} found`);
        hardcodedCount += nonI18nStrings.length;
      }
    }
  }

  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    files.forEach((file) => {
      const filePath = path.join(dir, file);
      if (fs.statSync(filePath).isDirectory()) {
        walkDir(filePath);
      } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
        checkFile(filePath);
      }
    });
  }

  walkDir(srcDir);

  if (hardcodedCount > 0) {
    console.warn(`\nFound ${hardcodedCount} potentially hardcoded strings. Use i18n.t() for user-facing text.`);
    console.log('Externalized strings check completed with warnings');
  } else {
    console.log('All strings properly externalized');
  }
}

checkExternalizedStrings();