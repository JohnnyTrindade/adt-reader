# Checklist de publicação

## 1. Antes de publicar
- [ ] Renomear a pasta `github-files` para `.github`. Ela contém o CI e os templates de issue; o Claude não consegue gravar direto em pastas `.github`.
- [ ] Decidir o nome final. `adtreader` / `adt-reader` são provisórios. Conferir se o nome está livre no PyPI (https://pypi.org/project/adtreader/) e no GitHub.
- [ ] Trocar `https://github.com/JohnnyTrindade/adt-reader` em `.github/ISSUE_TEMPLATE/sample-submission.yml`
- [ ] Rodar os testes localmente: `pip install -e ".[dev]"` e depois `pytest`.

## 2. Criar o repositório
No GitHub, crie um repositório público vazio (sem README nem licença, que já existem aqui). Depois, em `E:\claude_projects\adt-reader`:

```bash
git init -b main
git add .
git commit -m "adt-reader 0.0.2: initial public release"
git remote add origin https://github.com/JohnnyTrindade/adt-reader.git
git push -u origin main
```

- [ ] Conferir se o CI (aba Actions) passou
- [ ] Em Settings → General, adicionar descrição e topics: `advantage-database`, `ads`, `adt`, `reverse-engineering`, `data-migration`, `python`

## 3. Issue fixada pedindo amostras
- [ ] Criar uma issue com o título "Help wanted: sample .adt files for the remaining field types"
- [ ] Colar o texto de `docs/launch/issue-samples-wanted.md` (trocando `https://github.com/JohnnyTrindade/adt-reader`)
- [ ] Fixar a issue (Pin issue) e adicionar os labels `help wanted` e `samples`

## 4. Divulgação
Em todos os textos, troque `https://github.com/JohnnyTrindade/adt-reader` pela URL do repositório.

- [ ] Fórum X#: responder no tópico "Advantage Database Server (ADS) End of Life" usando `post-xsharp-forum.md`
- [ ] en.delphipraxis.net, seção de banco de dados (mesmo texto)
- [ ] Grupos brasileiros de Delphi e automação comercial, LinkedIn: `post-grupos-br.md`
- [ ] Opcional: abrir issues nos repositórios ruby-adt e node_adt avisando do projeto (eles têm usuários com o mesmo problema)

## 5. PyPI (depois das primeiras amostras)
- [ ] Criar conta no PyPI e configurar trusted publishing pelo GitHub Actions
- [ ] Publicar a versão 0.1.0 quando memo/money/timestamp estiverem verificados

## Quando chegar uma amostra
1. Colocar os `.adt`/`.adm` em `samples/`
2. Rodar `pytest`. O `tests/test_samples.py` compara cada tabela com os valores esperados.
3. Para cada falha, decidir se o leitor está errado ou o valor esperado era um palpite. Corrigir e atualizar o `docs/FORMAT.md`.
