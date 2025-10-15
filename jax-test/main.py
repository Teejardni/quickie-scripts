import numpy as np
import jax
import jax.numpy as jnp
import time

def custom_cosine_similarity(a, b):
    """
    Computes the cosine similarity between two matrices A and B, 
    where A and B are stacks of vectors (matrices).
    
    A: (N, D) matrix of N vectors of dimension D.
    B: (M, D) matrix of M vectors of dimension D.
    Returns: (N, M) matrix of cosine similarities.
    """
    # Normalize the vectors (L2 norm)
    norm_a = np.sqrt(np.sum(a**2, axis=1, keepdims=True))
    norm_b = np.sqrt(np.sum(b**2, axis=1, keepdims=True))
    
    norm_a = np.where(norm_a == 0, 1.0, norm_a)
    norm_b = np.where(norm_b == 0, 1.0, norm_b)
    
    similarity = (a @ b.T) / (norm_a @ norm_b.T)
    return similarity


def jax_cosine_similarity(a, b):
    """
    JAX version of the cosine similarity function.
    """
    norm_a = jnp.sqrt(jnp.sum(a**2, axis=1, keepdims=True))
    norm_b = jnp.sqrt(jnp.sum(b**2, axis=1, keepdims=True))
    
    norm_a = jnp.where(norm_a == 0, 1.0, norm_a)
    norm_b = jnp.where(norm_b == 0, 1.0, norm_b)
    
    similarity = (a @ b.T) / (norm_a @ norm_b.T)
    return similarity


# Compile the JAX version of the function for maximum performance
jit_cosine_similarity = jax.jit(jax_cosine_similarity)


def benchmark_function(func, a_data, b_data, name, num_runs=5):
    """Measures the execution time of a function."""
    times = []
    
    # For JAX JIT, we MUST perform a warm-up run to include the compilation time 
    # and ensure the second run is truly compiled.
    if "JIT" in name:
        func(a_data, b_data).block_until_ready() 
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        
        # Execute the function
        result = func(a_data, b_data)
        
        # JAX requires block_until_ready() to ensure the computation completes 
        # before we stop the timer, as JAX operations are asynchronous.
        if "JAX" in name:
            result.block_until_ready()
            
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000) # Convert to milliseconds (ms)
        
    return name, np.mean(times)


def run_benchmark():
    # The complexity is O(N * M * D), which is good for comparison.
    vector_dim = 768 
    sizes = [10, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500] # N and M will both be this size.

    print("--- Performance Comparison: Cosine Similarity (N x M matrices) ---")
    print(f"Vector Dimension (D): {vector_dim}\n")
    print(f"{'Size (N=M)':<10} | {'NumPy (ms)':<15} | {'JAX (non-JIT) (ms)':<20} | {'JAX (JIT) (ms)':<15}")
    print("-" * 70)

    for size in sizes:
        # Generate data for NumPy
        a_np = np.random.rand(size, vector_dim).astype(np.float32)
        b_np = np.random.rand(size, vector_dim).astype(np.float32)
        
        # Convert to JAX arrays for JAX tests
        a_jnp = jnp.asarray(a_np)
        b_jnp = jnp.asarray(b_np)

        # 1. NumPy Test (Using the standard numpy function, which is the baseline)
        name_np, time_np = benchmark_function(
            custom_cosine_similarity, a_np, b_np, "NumPy"
        )
        
        # 2. JAX (non-JIT) Test - The overhead of JAX without optimization
        name_jnp, time_jnp = benchmark_function(
            jax_cosine_similarity, a_jnp, b_jnp, "JAX (non-JIT)"
        )

        # 3. JAX (JIT) Test - The core advantage
        name_jit, time_jit = benchmark_function(
            jit_cosine_similarity, a_jnp, b_jnp, "JAX (JIT)"
        )
        
        # Output results
        print(f"{size:<10} | {time_np:<15.4f} | {time_jnp:<20.4f} | {time_jit:<15.4f}")

if __name__ == "__main__":
    run_benchmark()
