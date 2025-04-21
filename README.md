# **[WIP] Spectorin**

AI-powered formal verification and static analysis tool for smart contracts.

## Features

- Static analysis for multiple blockchain smart contract languages:
  - Solidity (Ethereum & EVM chains)
  - PyTeal (Algorand)
  - Move (Sui, Aptos)
  - Rust (Solana, Substrate/Polkadot)
- Security score calculation
- Actionable recommendations for improving security
- Formal verification using Z3 theorem prover
- Dynamic testing/fuzzing capabilities
- Web interface and CLI

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/spectorin.git
cd spectorin

# Install dependencies
poetry install
```

## Usage

### CLI

```bash
# Analyze a smart contract
poetry run python spectorin.py analyze run path/to/contract.sol --chain solidity

# Formally verify a property
poetry run python spectorin.py verify run path/to/contract.sol

# Run fuzzing tests
poetry run python spectorin.py test run path/to/contract.sol
```

### Web Interface

```bash
# Start the web server
cd ui
npm install
npm run dev

# In a separate terminal, start the API server
cd ..
poetry run uvicorn api.main:app --reload
```

Then visit http://localhost:3000 in your browser.

## Example

```bash
# Analyze a Solidity contract
poetry run python spectorin.py analyze run examples/solidity_example.sol --chain solidity

# Analyze a PyTeal contract
poetry run python spectorin.py analyze run examples/pyteal_example.py --chain pyteal
```

## Security Score

The security score is calculated based on the number and severity of issues found:
- 100: No issues found
- 80-99: Minor issues
- 50-79: Moderate issues
- 0-49: Severe issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
