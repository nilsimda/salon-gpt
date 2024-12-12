import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: 'http://0.0.0.0:8000/openapi.json',
  output: './src/salon-client/generated',
  name: 'SalonClientGenerated',
  types: {
    enums: 'typescript',
  },
  services: {
    asClass: true,
  },
});
