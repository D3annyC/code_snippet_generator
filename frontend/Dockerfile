FROM node:18.19.0

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Angular CLI
RUN npm install -g @angular/cli@17.3.0

# Install app dependencies
RUN npm install

# Make port 4200 available to the world outside this container
EXPOSE 4200

# Run the app
CMD ["npm","run", "start"]
