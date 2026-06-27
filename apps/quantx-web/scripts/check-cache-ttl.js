const fs = require('fs');
const path = require('path');

const CACHE_TTL_MINUTES = 5;

function checkCacheTTL() {
  const cacheDir = path.join(__dirname, '../src/shared/cache');
  const files = fs.readdirSync(cacheDir);
  let hasErrors = false;

  files.forEach((file) => {
    if (file.endsWith('.ts')) {
      const content = fs.readFileSync(path.join(cacheDir, file), 'utf8');
      
      const ttlMatches = content.match(/ttl:\s*(\d+)/g);
      if (ttlMatches) {
        ttlMatches.forEach((match) => {
          const ttl = parseInt(match.split(':')[1].trim(), 10);
          if (ttl <= 0) {
            console.error(`Error: Cache TTL must be positive in ${file}: ${match}`);
            hasErrors = true;
          } else if (ttl > CACHE_TTL_MINUTES * 60000) {
            console.warn(`Warning: Cache TTL exceeds ${CACHE_TTL_MINUTES} minutes in ${file}: ${match}`);
          }
        });
      }

      if (content.includes('cacheTime:') && !content.includes('staleTime:')) {
        console.error(`Error: Cache must have TTL (staleTime) defined in ${file}`);
        hasErrors = true;
      }
    }
  });

  if (hasErrors) {
    console.error('\nCache TTL check failed');
    process.exit(1);
  }
  
  console.log('Cache TTL check passed');
}

checkCacheTTL();