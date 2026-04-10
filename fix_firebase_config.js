const fs = require('fs');
const path = 'firebase-functions/index.js';
let content = fs.readFileSync(path, 'utf8');

// Replace dashscope.key with qwen.api_key
content = content.replace('functions.config().dashscope.key', 'functions.config().qwen.api_key');

fs.writeFileSync(path, content);
console.log('Fixed API key reference in index.js');
