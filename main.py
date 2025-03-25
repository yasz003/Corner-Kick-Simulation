from optimization import optimize_corner_kick_parameters

def main():
    print("Starting corner kick optimization simulation...")
    optimal_params = optimize_corner_kick_parameters()
    
    if optimal_params is None:
        print("Optimization failed to find valid solutions.")
        return
    
    print("\nOptimization completed successfully!")

if __name__ == "__main__":
    main()