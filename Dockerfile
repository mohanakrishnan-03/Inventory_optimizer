# Step 1: Use official Node.js image
FROM node:18

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Step 4: Copy all project files into container
COPY . .

# Step 5: Expose port 3000
EXPOSE 3000

# Step 6: Run the app
CMD ["npm", "start"]
