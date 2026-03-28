# Binance Trading Bot (MVP)

Projeto inicial para automação de estratégias em **Spot** e **Futures** na Binance, com foco em:

- execução sem emocional;
- gestão de risco obrigatória;
- separação clara entre estratégia, risco e execução.

> ⚠️ Uso educacional. Operar em mercado real envolve risco.

## Estrutura

```text
binance-bot/
  src/
    main.py
    config/settings.py
    data/binance_client.py
    strategy/base.py
    strategy/wyckoff_stub.py
    risk/manager.py
    execution/executor.py
    core/engine.py
```

## Como rodar

1. Crie um ambiente virtual Python 3.11+
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis de ambiente (copie `.env.example` para `.env`).
4. Rode em modo paper:

```bash
python -m src.main --symbol BTCUSDT --market futures --mode paper
```

## Próximos passos

- implementar regras objetivas de Wyckoff em `strategy/wyckoff_stub.py`;
- adicionar persistência em banco de dados;
- adicionar backtest e dashboard;
- integrar Binance Testnet para validação de ordens.
