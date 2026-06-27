module.exports = {
  rules: {
    'flag-naming': {
      create: (context: any) => ({
        Identifier(node: any) {
          const flagPattern = /^[a-z]+\.[a-z]+\.[a-z]+$/;
          if (typeof node.name === 'string' && node.name.includes('flag')) {
            if (!flagPattern.test(node.name) && !node.name.startsWith('FLAG_CONFIG')) {
              context.report({
                node,
                message: 'Flag keys must follow {domain}.{feature}.{variant} pattern per MDS 54.4',
              });
            }
          }
        },
      }),
    },
    'cache-keys': {
      create: (context: any) => ({
        CallExpression(node: any) {
          if (
            node.callee.type === 'Identifier' &&
            node.callee.name === 'createCacheKey'
          ) {
            if (!node.arguments[0]?.properties) {
              context.report({
                node,
                message: 'Cache keys must follow namespaced format per MDS 53.3',
              });
            }
          }
        },
      }),
    },
  },
};