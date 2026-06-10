# quant2

Simulator and teacher of quantum computing — illustrates basic concepts and lets you write and simulate quantum programs.

## Installation

```bash
git clone <repo url>
cd quant2
uv sync
```

## Usage

```bash
uv run <entry point>
```

## Development

```bash
uv run pytest
```

## License

MIT — see [LICENSE](LICENSE)


### Qbits

These are Quantum Bits. They don't have a known value until they are "read" at which point they "collapse". They collapse to either 1 or 0, probabilistically. 

So if I create the same Qbit 1000 times and read it over and over, I will get a mix of zeros and ones.
