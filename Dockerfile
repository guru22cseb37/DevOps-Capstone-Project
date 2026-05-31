# ==============================================================================
#  Stage 1: Build & Dependencies
# ==============================================================================
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

# Copy dependency manifests
COPY app/package*.json ./

# Install all dependencies (including devDependencies if linting/tests are needed)
RUN npm ci

# Copy application source code
COPY app/ ./

# ==============================================================================
#  Stage 2: Minimalist Production Environment
# ==============================================================================
FROM node:20-alpine AS runner

# Set production node environment
ENV NODE_ENV=production
WORKDIR /usr/src/app

# Create a non-privileged user and group for application security
RUN addgroup -g 1001 -S nodejs && \
    adduser -u 1001 -S nodejs -G nodejs

# Copy dependency manifest and build results from Stage 1
COPY --from=builder /usr/src/app/package*.json ./
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/src ./src
COPY --from=builder /usr/src/app/public ./public

# Ensure appropriate ownership of the working directories
RUN chown -R nodejs:nodejs /usr/src/app

# Run the container under the non-root nodejs user
USER nodejs

# Expose Express server telemetry ports
EXPOSE 3000

# Server launch command
CMD ["npm", "start"]
