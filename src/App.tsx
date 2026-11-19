import React, { useState, useEffect } from "react";
import axios from "axios";

interface Product {
  id: string;
  name: string;
  priceCents: number;
  imageEmoji: string;
}

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    axios.get("/api/products").then((res) => {
      setProducts(res.data);
    });
  }, []);

  return (
    <div>
      <h1>Products</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.imageEmoji} {product.name} - ${(product.priceCents / 100).toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}
