# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source files
COPY . .

# Build the app
RUN npm run build

# Verify build output
RUN ls -la dist/

EXPOSE 3000

# Use Vite preview
CMD ["npm", "run", "preview"]