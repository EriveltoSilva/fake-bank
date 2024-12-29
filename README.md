# fake-bank


## Fake Bank Possible Operations

### **Gestão de Contas**
1. **abrir_conta**
   - Abertura de conta corrente(user, account_type, account_number,iban, balance).

2. **transferir_dinheiro**
   - Realiza transferências entre contas do mesmo banco ou para outros bancos (via IBAN).

3. **consultar_detalhes_conta**
   - Exibe informações sobre titular, tipo de conta, número da conta e iban.


### **Operações Bancárias**
5. **consultar_saldo**
   - Exibe o saldo disponível em conta corrente e poupança.

6. **consultar_historico_transacoes**
   - Mostra um resumo das últimas transações realizadas, com filtros por data e tipo.


//-------------------------------------------------
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



<h2 id="routes">📍 API Endpoints </h2>

Here is a comprehensive list of the primary API endpoints, along with the expected request bodies and responses for each route.

<h3> Account </h3>

| Route                                  | Description                                         |
|----------------------------------------|-----------------------------------------------------|
| <kbd> POST /bank/accounts/create/ </kbd>       | Create customer account                          |
| <kbd> GET /bank/accounts/details/{int:account_number}/ </kbd>     | Get account detail customer account number |
| <kbd> GET /bank/accounts/details/iban/{str:iban}/ </kbd>     | Get account detail by customer iban |


<h3> POST /bank/accounts/create/ </h3>

**REQUEST BODY**
```json
{
    "balance": 12300.34,
    "account_type": "checking",
    "user": {
        "full_name": "Jonh Doe",
        "username": "jonh.doe",
        "email": "jonh.doe@gmail.com",
        "phone": "940000002",
        "password": "123456789",
        "confirmation_password": "123456789"
    }
}
```

**RESPONSE**
```json
{
    "id": 2,
    "account_type": "checking",
    "account_number": 7248749154545,
    "iban": "AO06004000007248749154545",
    "balance": "12300.34",
    "created_at": "2024-12-29T18:00:07.313180+01:00",
    "user": {
        "uid": "8aca2d21-f1ad-49c0-b55a-21c39b895225",
        "full_name": "Jonh Doe",
        "email": "jonh.doe@gmail.com",
        "username": "jonh.doe",
        "phone": "940000002",
        "profile": 3
    }
}
```


<h3> GET /bank/accounts/details/{int:account_number}/ </h3>

**RESPONSE**
```json
{
    "id": 3,
    "account_type": "checking",
    "account_number": 5827575850450,
    "iban": "AO06004000005827575850450",
    "balance": "12300.34",
    "created_at": "2024-12-29T18:04:44.464664+01:00",
    "user": {
        "uid": "6ca07501-3c92-4632-b4ee-e1c62bedc8fc",
        "full_name": "Jonh Doe",
        "email": "jonh.doe@gmail.com",
        "username": "jonh.doe",
        "phone": "940000002",
        "profile": 4
    }
}
```

<h3> GET /bank/accounts/details/iban/{int:iban}/ </h3>

**RESPONSE**
```json
{
    "id": 3,
    "account_type": "checking",
    "account_number": 5827575850450,
    "iban": "AO06004000005827575850450",
    "balance": "12300.34",
    "created_at": "2024-12-29T18:04:44.464664+01:00",
    "user": {
        "uid": "6ca07501-3c92-4632-b4ee-e1c62bedc8fc",
        "full_name": "Jonh Doe",
        "email": "jonh.doe@gmail.com",
        "username": "jonh.doe",
        "phone": "940000002",
        "profile": 4
    }
}
```



<h3> POST /bank/transfer/account-number/ </h3>

**REQUEST BODY**
```json
{
    "transfer_type":"credit",
    "sender_account_number": "5827575850450",
    "receiver_account_number": "6316101549399",
    "amount": 40.00
}
```

**RESPONSE**
```json
{
    "message": "Transferência realizada com sucesso!",
    "transfer_details": {
        "sender_name": "Jonh Doe",
        "sender_account": 5827575850450,
        "receiver_account": 6316101549399,
        "receiver_name": "Pascoal Moniz",
        "amount": 40.0,
        "transaction_id": "5b44f071-9aff-4b48-bf94-a7635437e81c",
        "transfer_type": "credit",
        "created_at": "2024-12-29T17:55:18.701322Z"
    }
}
```


<h3> POST /bank/transfer/iban/ </h3>

**REQUEST BODY**
```json
{
    "transfer_type":"credit",
    "sender_iban": "AO06004000005827575850450",
    "receiver_iban": "AO06004000006316101549399",
    "amount": 40.00
}
```

**RESPONSE**
```json
{
    "message": "Transferência realizada com sucesso!",
    "transfer_details": {
        "sender_name": "Jonh Doe",
        "sender_account": "AO06004000005827575850450",
        "receiver_account": "AO06004000006316101549399",
        "receiver_name": "Pascoal Moniz",
        "amount": 40.0,
        "transaction_id": "8b9f67ec-3b19-4c05-9a5a-0cf6e0c49441",
        "transfer_type": "credit",
        "created_at": "2024-12-29T17:50:32.071630Z"
    }
}
```

