# Base image
FROM node

# Set working directory
WORKDIR /usr/app

# Copy .json files
COPY package*.json ./

# Install dependecies
RUN npm install

# Copy remaining files
COPY ./ ./

# Build project
RUN npm run build