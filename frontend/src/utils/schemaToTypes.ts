import { JSONSchema7 } from 'json-schema';
import { compile } from 'json-schema-to-typescript';
import fs from 'fs';
import path from 'path';

/**
 * Generate TypeScript types from JSON schema
 * @param schemaPath Path to JSON schema file
 * @param outputPath Path to output TypeScript file
 */
export async function generateTypesFromSchema(
  schemaPath: string,
  outputPath: string
): Promise<void> {
  try {
    // Read schema file
    const schema = JSON.parse(
      fs.readFileSync(schemaPath, 'utf8')
    ) as JSONSchema7;

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

    // Write TypeScript file
    fs.writeFileSync(outputPath, ts);
    console.log(`Generated ${outputPath} from ${schemaPath}`);
  } catch (error) {
    console.error(`Error generating types from schema: ${error}`);
    throw error;
  }
}

// Example usage:
// generateTypesFromSchema(
//   '../schemas/simulation_config_schema.json',
//   './src/types/SimulationConfig.ts'
// );
// generateTypesFromSchema(
//   '../schemas/simulation_result_schema.json',
//   './src/types/SimulationResult.ts'
// );
