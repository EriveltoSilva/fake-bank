# Pontos do Luena v2.


- Bloquear todas as rotas importantes
- Pegar detalhes da conta pelo user autenticado


## **Gestão de Contas**
1. **abrir_conta_corrente**
   - Abertura de conta corrente, coleta de informações pessoais e validação de documentos.

2. **abrir_conta_poupanca**
   - Orientação e registro para abertura de conta poupança.

3. **consultar_detalhes_conta**
   - Exibe informações sobre tipo de conta, agência, número da conta e titular.

4. **alterar_dados_cadastrais**
   - Atualização de informações pessoais, como endereço, e-mail e telefone.


## **Operações Bancárias**
5. **consultar_saldo**
   - Exibe o saldo disponível em conta corrente e poupança.

6. **consultar_historico_transacoes**
   - Mostra um resumo das últimas transações realizadas, com filtros por data e tipo.

7. **transferir_dinheiro**
   - Realiza transferências entre contas do mesmo banco ou para outros bancos (via IBAN).

8. **pagar_conta**
   - Permite o pagamento de faturas, boletos ou contas com leitura de código de barras.

9. **recarga_celular**
   - Recarga de créditos para telefones móveis, diretamente do saldo bancário.

10. **consultar_empréstimos**
    - Mostra informações sobre empréstimos ativos e simula novos empréstimos.

11. **solicitar_emprestimo**
    - Inicia o processo para solicitar um empréstimo, com cálculo de parcelas e aprovação online.

12. **investir**
    - Orientação e registro para investimentos em poupança, CDBs ou fundos.



## **Gestão de Cartões**
13. **consultar_saldo_cartao**
    - Exibe o saldo disponível no cartão de crédito ou débito.

14. **consultar_fatura_cartao**
    - Mostra a fatura atual e as transações realizadas no cartão de crédito.

15. **bloquear_cartao**
    - Bloqueia o cartão em caso de perda, roubo ou suspeita de fraude.

16. **desbloquear_cartao**
    - Auxilia no desbloqueio do cartão.

17. **pedir_cartao**
    - Solicitação de um novo cartão ou substituição de cartão danificado.



## **Segurança e Suporte**
18. **alterar_senha**
    - Permite alterar a senha da conta ou do cartão.

19. **denunciar_fraude**
    - Canal para reportar atividades suspeitas ou transações não autorizadas.

20. **autenticar_usuario**
    - Verifica a identidade do usuário antes de realizar transações sensíveis.



## **Suporte e Atendimento**
21. **falar_com_atendente**
    - Conecta o cliente com um atendente humano.

22. **encontrar_agencia**
    - Fornece informações sobre a agência mais próxima com base na localização.

23. **consultar_taxas_juros**
    - Exibe as taxas de juros vigentes para serviços bancários.

24. **alterar_limite_cartao**
    - Permite ajustar o limite do cartão de crédito.

25. **consultar_cambio**
    - Informa as taxas de câmbio atuais e realiza conversões entre moedas.



## **Funcionalidades Avançadas**
26. **gerar_extrato_pdf**
    - Gera um extrato em PDF para download ou envio por e-mail.

27. **notificacoes_transacoes**
    - Configura alertas de transações via SMS ou e-mail.

28. **gerar_qr_code_pagamento**
    - Gera QR Codes para pagamentos rápidos em lojas ou transferências.

29. **agendar_pagamento**
    - Permite agendar transferências ou pagamentos recorrentes.

30. **consultar_programa_fidelidade**
    - Mostra pontos acumulados em programas de recompensas e como utilizá-los.


## **Acessibilidade e Personalização**
31. **ajustar_configuracoes**
    - Personaliza o idioma, notificações e configurações de acessibilidade.

32. **assistente_virtual_educacional**
    - Ensina o usuário como usar serviços bancários online, como TED, PIX ou transferência internacional.

33. **ativar_funcao_multicanal**
    - Integra o bot em diferentes canais, como WhatsApp, site ou aplicativo móvel.

34. **feedback**
    - Solicita a opinião do cliente para melhorar o serviço.


1. Defining the Purpose(Bot hibrido:Transacional e Informativo)
Luena é um assistente virtual(bot) criado com o objectivo de:
	- Dar suporte
	- Assistência ao cliente
	- Prover informações(FAQs),
	- Servir como o primeiro bot bancário transacional
atuando e interagindo com os clientes BAI nos mais diversos canais:
	1. Website
	2. Whatsapp
	3. BAI Direto


2. Designing Conversations Flows
	- Intents:
		1. Abrir de Conta
		2. Consultar saldo.
		3. Ver(Consultar) detalhes da Conta
		4. Ver histórico de Transações
		5. Ver detalhe da transação XYZ
		5. Bloquear Cartão
		6. Transferências (Transferir, Transferir fundos)
	- FAQs(Dúvidas frequentes)

