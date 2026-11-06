# What is Jito?
Turbocharged Solana trading experience.

# What does Jito offer?
  - **Low latency transaction sending**
  - **Market maker priority**
  - **Preconfirmations**
  - **Developer support**

# Who should use Jito?
- **Applications**
- **High Frequency Traders**
- **Transaction landing services**

If your use case requires low-latency transaction sending, MEV protection, and/or cross-transaction
atomicity, then Jito is right for you.

## Jito's Products
Jito provides specialized solutions tailored to the needs of Solana MEV users:
- 🌪️ **[FullSend](fullsend.md):** Ultra low-latency transaction sending, essential for applications on Solana with high volume, throughput, and privacy needs.
- 💼 **[Bundles](bundles.md):** Offers MEV protection, fast transaction landing, support for multiple transactions, and revert protection, making it ideal for developers of HFT and other automated trading systems.
- 👨🏻‍🍳 **[Maker priority](https://bam.dev/docs/bam/maker-plugin/how-it-works/):** A dedicated, priority transaction ingress path for enrolled market makers. It provides top-of-batch scheduling for market maker transactions.
- ⚡ **[Preconfirmations](https://bam.dev/docs/bam/preconfirmations/):** Ultra low-latency confirmation results from BAM nodes that are further upstream and faster than Solana shreds.

These use cases offer a competitive edge to searchers, market makers, applications, and anyone seeking MEV protection.

```{toctree}
:maxdepth: 6
:hidden:
:caption: BAM

🌪️ FullSend <fullsend>
💼 Bundles <bundles>
👨🏻‍🍳 Maker Priority (MPP) <mpp>
⚡ Preconfirmations <preconfirmations>
```

```{toctree}
:maxdepth: 6
:hidden:
:caption: Block Engine

🌪️ Low Latency Transaction Send <lowlatencytxnsend>
```

```{toctree}
:maxdepth: 6
:hidden:
:caption: Legal

⚖️ Legal <legal>
```
