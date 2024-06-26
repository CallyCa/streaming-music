const esbuild = require('esbuild');
const { globPlugin } = require('esbuild-plugin-glob');

// Função para construir com esbuild
async function buildWithEsbuild() {
  try {
    await esbuild.build({
      entryPoints: [
        'tests/simulations/graphql/load.test.js',
        'tests/simulations/graphql/endurance.test.js',
        'tests/simulations/rest/endurance.test.js',
        'tests/simulations/rest/load.test.js',
        'tests/simulations/rest/stress.test.js',
      ],
      bundle: true,
      outdir: 'dist',
      platform: 'node',
      sourcemap: true,
      plugins: [globPlugin()],
      target: 'esnext',
      format: 'cjs',
      external: ['k6'],
      minify: process.env.NODE_ENV === 'production',
    });
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

// Função para assistir mudanças nos arquivos e reconstruir
async function watchFiles() {
  // Inicializa a construção inicial
  await buildWithEsbuild();

  // Assiste por mudanças nos arquivos e reconstrói quando necessário
  const chokidar = require('chokidar');
  const watcher = chokidar.watch(['tests/**/*.js']);

  watcher.on('change', async () => {
    console.log('Arquivos modificados. Reconstruindo...');
    await buildWithEsbuild();
  });
}

// Verifica se está em modo de desenvolvimento
const isDevelopment = process.env.NODE_ENV === 'development';

// Executa o modo de watch se estiver em desenvolvimento
if (isDevelopment) {
  watchFiles();
} else {
  buildWithEsbuild();
}
