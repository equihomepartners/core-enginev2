#!/usr/bin/env node

import { compile } from 'json-schema-to-typescript';
import fs from 'fs';
import path from 'path';

/**
 * Generate TypeScript types from JSON schema
 * @param {string} schemaPath Path to JSON schema file
 * @param {string} outputPath Path to output TypeScript file
 */
async function generateTypesFromSchema(schemaPath, outputPath) {
  try {
    // Read schema file
    const schema = JSON.parse(
      fs.readFileSync(schemaPath, 'utf8')
    );

    // Compile schema to TypeScript
    const ts = await compile(schema, schema.title || 'Schema', {
      bannerComment: `/**
 * This file was automatically generated from ${path.basename(schemaPath)}
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run the generator again.
 */`,
      style: {
        singleQuote: true,
        semi: true,
        tabWidth: 2,
        trailingComma: 'es5',
        printWidth: 100,
      },
    });

    // Create directory if it doesn't exist
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Write TypeScript file
    fs.writeFileSync(outputPath, ts);
    console.log(`Generated ${outputPath} from ${schemaPath}`);
  } catch (error) {
    console.error(`Error generating types from schema: ${error}`);
    process.exit(1);
  }
}

// Generate types for simulation config
generateTypesFromSchema(
  '../schemas/simulation_config_schema.json',
  './src/types/SimulationConfig.ts'
);

// Generate types for simulation result
generateTypesFromSchema(
  '../schemas/simulation_result_schema.json',
  './src/types/SimulationResult.ts'
);
