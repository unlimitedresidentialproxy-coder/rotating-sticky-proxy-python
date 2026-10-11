# Rotating and Sticky Residential Proxy Sessions in Python

Practical `requests` examples for two common residential proxy session modes:

- **Rotating sessions** for independent requests that can use different available exits.
- **Sticky sessions** for multi-step workflows that should keep one exit during a session window.

Use these examples only for authorized automation and respect each target’s terms, rate limits, and applicable laws.

## Install

```bash
python -m pip install requests
```

For SOCKS5 support:

```bash
python -m pip install "requests[socks]"
```

## Environment variables

Never commit proxy credentials. Set them in your environment:

```bash
PROXY_HOST=<YOUR_GATEWAY_HOST>
PROXY_PORT=7777
PROXY_USER=<YOUR_USERNAME>
PROXY_PASS=<YOUR_PASSWORD>
```

## Rotating requests

Run:

```bash
python rotating_session.py
```

The gateway controls rotation behavior. Access to a pool does not guarantee a unique IP on every request.

## Sticky sessions

Run:

```bash
python sticky_session.py
```

The example appends a session identifier to the username using a generic placeholder format. Replace `build_sticky_username()` with the session syntax documented for your gateway account.

A sticky session is not permanent: the exit can change when the session expires, becomes unavailable, or reconnects.

## Production checklist

- Use explicit connection and read timeouts.
- Retry only transient failures with bounded exponential backoff.
- Never log credentials.
- Increase concurrency gradually.
- Track success rate, response latency, retry rate, and actual throughput.
- Confirm location availability before time-sensitive work.

## Planning bandwidth

Session mode and bandwidth solve different problems. Estimate throughput from response size, request rate, active hours, concurrency, and retry overhead.

- [Developer documentation](https://unlimitedresidentialproxy.com/documentation)
- [Residential proxy bandwidth calculator](https://unlimitedresidentialproxy.com/calculator)
- [Unlimited residential proxy plans](https://unlimitedresidentialproxy.com/pricing)

The listed no-data-cap plans provide aggregate throughput tiers from 100 Mbps to 1 Gbps for 1, 7, or 30 days, with rotating or sticky sessions and access to a shared pool of more than 4 million residential IPs.
