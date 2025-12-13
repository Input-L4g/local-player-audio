# Player de Áudio em Python — Modelo Simples

Este projeto consiste em um **player de áudio em Python**, desenvolvido com foco em **aprendizado, organização de código e arquitetura**, priorizando baixo consumo de recursos e separação clara de responsabilidades.

Este **modelo simples** serve como base sólida para evoluções futuras (CLI avançado e GUI), sem incluir funcionalidades complexas ou dependências pesadas.

---

## Objetivo do Modelo

- Reproduzir músicas locais de forma confiável
- Manter código modular, legível e extensível
- Servir como laboratório de arquitetura e boas práticas
- Funcionar corretamente em ambientes Linux
- Evitar soluções infladas ou acopladas à interface

---

## Funcionalidades

### Reprodução de Áudio
- Reprodução de arquivos de áudio locais
- Suporte aos formatos permitidos pela biblioteca de áudio utilizada
- Controles básicos:
  - Play
  - Pause
  - Stop
  - Próxima faixa
  - Faixa anterior
- Controle de volume (escala linear)

---

### Playlist
- Playlist única
- Persistência local em arquivo JSON
- Operações disponíveis:
  - Adicionar arquivos
  - Remover arquivos
  - Reordenar faixas
  - Limpar playlist
- Playlist mantida entre execuções do programa

---

### Modos de Reprodução
- Sequencial (ordem natural da playlist)
- Aleatório (shuffle)
- Loop:
  - Loop da playlist completa
  - Loop da faixa atual

---

### Navegação de Arquivos (CLI)
- Navegação interativa pelo sistema de arquivos via terminal
- Seleção manual de arquivos de áudio
- Não há indexação automática de pastas
- Caminhos são resolvidos para paths absolutos antes da persistência

---

### Interface
- Interface em linha de comando (CLI)
- Exibição de informações básicas:
  - Música atual
  - Estado do player
  - Modo de reprodução ativo
- Interação por menus ou prompts interativos
- Não há atalhos globais de teclado

---

### Persistência
- Uso de JSON para:
  - Playlist
  - Configurações básicas (volume, modos)
- Tratamento de erros para:
  - Arquivos inexistentes
  - Arquivos corrompidos
  - Falhas de leitura e escrita

---

## Arquitetura do Projeto

Estrutura modular planejada:

```bash
src/
    core/
        player.py           # Motor de áudio
        playlist.py         # Lógica da playlist
        controller.py       # Estados e regras de controle

    ui/
        player_screen.py    # Cena principal do player
        screen_manager.py   # Controle de fluxo entre cenas
        base_screen.py      # Contrato base das cenas

    utils/
        files_utils.py      # Manipulação de arquivos
        errors_utils.py     # Exceções e validações
        paths_utils.py      # Resolução de caminhos

    resources/
        config.json         # Configurações persistentes
        playlist.json       # Dados da playlist

tests/
    ...                     # Testes automatizados via pytest
```

### Princípios Arquiteturais
- Separação total entre lógica e interface
- Core independente da UI
- Código testável e reutilizável
- Baixo acoplamento entre módulos

---

## Limitações Deliberadas do Modelo
- Não há streaming
- Não há múltiplas playlists
- Não há banco de dados
- Não há interface gráfica
- Não há sistema de plugins
- Não há efeitos de áudio

Essas funcionalidades são reservadas para modelos futuros.

---

## Critérios de Sucesso
- Execução estável em Linux
- Baixo consumo de memória
- Código organizado e de fácil manutenção
- Base consistente para evolução incremental do projeto

---

## Observação Final
Este modelo não tem como objetivo ser um produto final, mas sim uma fundação técnica bem definida para estudo e expansão controlada.
