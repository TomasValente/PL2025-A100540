# PL2025-TPC4

## Data: 06/03/2025

## Autor

![defpfp]

**Nome:** João Tomás Gonçalves de Sousa Carneiro Valente

**Número:** A100540

**Email:** a100540@alunos.uminho.pt

## Objetivos
- **Analisador Léxico**
    - Construir um analisador léxico para uma liguagem de `query` com a qual se podem escrever frases do género:

```
    # DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```
        

## Compilação
- **Input:** `python3 main.py`
- **Output:** O *output* é exibido no *stdin*.

## Resolução do problema
- **Módulos:**
    - **main.py:** Módulo responsável por analisar o texto de *input* e apresentar o resultado ao utilizador.

[defpfp]: https://cdn.discordapp.com/attachments/945777436543565905/1339688481852620940/8PoNI3aPnN1OwAAAAASUVORK5CYII.png?ex=67afa1a0&is=67ae5020&hm=611a110527f81b29368cd857610d53456005ee7132e42634ae455bb47fb36ced&