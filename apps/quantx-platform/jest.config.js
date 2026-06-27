{
  "testEnvironment": "node",
  "transform": {
    "^.+\\.tsx?$": ["ts-jest", {
      "tsconfig": "tsconfig.json"
    }]
  },
  "moduleFileExtensions": ["ts", "tsx", "js", "jsx", "json", "node"],
  "collectCoverageFrom": [
    "src/**/*.ts",
    "!src/**/*.module.ts",
    "!src/main.ts",
    "!src/**/*.interface.ts",
    "!src/**/*.enum.ts"
  ],
  "coverageDirectory": "../coverage",
  "testMatch": [
    "**/test/**/*.test.ts",
    "**/test/**/*.spec.ts"
  ]
}