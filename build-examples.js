import path from 'path';
import { fileURLToPath } from 'url';

import vfs from 'vinyl-fs';
import through from 'through2';
import glob from 'fast-glob';
import { rimraf } from 'rimraf';

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const exampleDir = path.join(currentDir, 'examples');
const snippetsDir = path.join(currentDir, 'snippets', 'examples');
const extMap = {
    '.dart': 'dart',
    '.js': 'javascript',
    '.json': 'json',
    '.py': 'python',
    '.sh': 'bash',
    '.ts': 'typescript',
    '.yml': 'yaml',
};
const ignore = [
    `${exampleDir}/**/node_modules`,
    `${exampleDir}/**/package.json`,
    `${exampleDir}/**/package-lock.json`,
    `${exampleDir}/**/yarn.lock`,
    `${exampleDir}/**/*.test.*`,
    `${exampleDir}/**/*.spec.*`,
    `${exampleDir}/**/*.mdx`, // Ignore existing MDX files
];

const map = through.obj((file, enc, cb) => {
    const parsed = path.parse(file.path);
    const type = extMap[parsed.ext];

    if (!type) {
        return;
    }

    const tabname = type.charAt(0).toUpperCase() + type.slice(1);

    parsed.base = `${parsed.name}.mdx`;
    parsed.ext = '.mdx';

    file.path = path.format(parsed);
    file.contents = Buffer.from(
        `\`\`\`${type} ${tabname}\n${file.contents.toString('utf-8')}\n\`\`\``
    );

    cb(null, file);
});

async function main() {
    try {
        await rimraf(snippetsDir);

        const entries = await glob(`${exampleDir}/**/*`, { ignore });

        vfs
            .src(entries, { base: exampleDir })
            .pipe(map)
            .pipe(vfs.dest(snippetsDir));

    } catch (error) {
        console.error('Error processing examples:', error);
    }
}

main();
