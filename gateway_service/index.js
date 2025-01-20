import {ApolloGateway, IntrospectAndCompose} from "@apollo/gateway";
import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import dotenv from "dotenv";

dotenv.config();

// Create the Apollo Gateway
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
       { name: "products", url: process.env.FEDERATED_SERVICES_PRODUCTS },
       { name: "images", url: process.env.FEDERATED_SERVICES_IMAGES },
    ],
  }),
});

const server = new ApolloServer({
  gateway,
});

// Start the Apollo Server
const { url } = await startStandaloneServer(server, {
  listen: { port: parseInt(process.env.PORT || "4000") },
});

console.log(`🚀 Apollo Gateway ready at ${url}`);