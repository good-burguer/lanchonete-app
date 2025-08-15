

 # 🌱 Fluxo de Trabalho com Git (Feature Branches)
 
 Este documento descreve o processo recomendado para trabalhar com Git no projeto **Sistema de Autoatendimento da Lanchonete** utilizando branches de funcionalidade.
 
 ---
 
 ## ✅ Passo a Passo para Desenvolver com Segurança
 
 ### 1. Atualize sua branch `main` local
 Antes de começar qualquer nova funcionalidade, garanta que a `main` está atualizada:
 
 ```bash
 git checkout main
 git pull origin main
 ```
 
 ---
 
 ### 2. Crie uma nova branch para sua funcionalidade
 A nova branch deve ser criada a partir da `main` atualizada:
 
 ```bash
 git checkout -b feature/nome-da-sua-feature
 ```
 
 Exemplo:
 ```bash
 git checkout -b feature/testes-clientes
 ```
 
 ---
 
 ### 3. Faça suas alterações e commits
 Implemente as mudanças normalmente. Ao finalizar uma parte, faça um commit:
 
 ```bash
 git add .
 git commit -m "feat: descrição da mudança"
 ```
 
 ---
 
 ### 4. Suba a branch para o repositório remoto
 ```bash
 git push -u origin feature/nome-da-sua-feature
 ```
 
 ---
 
 ### 5. Crie um Pull Request (PR)
 No GitHub, abra um PR comparando sua branch com a `main`. Após revisão e aprovação, realize o merge.
 
 ---
 
 ### 6. Atualize a `main` local após o merge
 ```bash
 git checkout main
 git pull origin main
 ```
 
 ---
 
 ### 7. (Opcional) Remova a branch local e remota
 ```bash
 git branch -d feature/nome-da-sua-feature
 git push origin --delete feature/nome-da-sua-feature
 ```
 
 ---
 
 ## ⚠️ Evite:
 
 - Fazer alterações direto na `main`.
 - Criar a feature branch antes de atualizar a `main`.
 - Commits pendentes antes de trocar de branch.
 - Esquecer de subir a branch antes de abrir o Pull Request.
 
 ---