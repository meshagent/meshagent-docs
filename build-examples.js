import path from 'path';
import { fileURLToPath } from 'url';

import vfs from 'vinyl-fs';
import through from 'through2';
import glob from 'fast-glob';

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const exampleDir = path.join(currentDir, 'examples');
const extMap = {
    '.dart': 'dart',
    '.js': 'javascript',
    '.json': 'json',
    '.py': 'python',
    '.sh': 'bash',
    '.ts': 'typescript',
    '.yml': 'yaml',
};
const ignore = [`${exampleDir}/javascript/node_modules`];

const map = through.obj((file, enc, cb) => {
    const parsed = path.parse(file.path);
    const type = extMap[parsed.ext];

    if (!type) {
        throw new Error(`Unsupported file type: ${parsed.ext}`);
    }

    const tabname = type.charAt(0).toUpperCase() + type.slice(1);

    parsed.base = parsed.name + '.mdx';
    parsed.ext = '.mdx';

    file.path = path.format(parsed);
    file.contents = Buffer.from(
        `\`\`\`${type} ${tabname}\n${file.contents.toString('utf-8')}\n\`\`\``
    );

    cb(null, file);
});

try {
    glob(`${exampleDir}/**/*`, { ignore }).then(entries => vfs
        .src(entries, { base: exampleDir })
        .pipe(map)
        .pipe(vfs.dest(path.join(currentDir, 'snippets'))));

} catch (error) {
    console.error('Error processing examples:', error);
}
