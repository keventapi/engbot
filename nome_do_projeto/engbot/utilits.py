from google import genai
from .models import Chat, Message

class AI():
    def __init__(self):
        key="AIzaSyARTBuxcO2KjU1BvdkDRac_Glq2Ppybqek"
        self.client = genai.Client(api_key=key)
        self.exemplo_relatorio = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório Técnico de Obra</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 40px;
    }
    h1, h2 {
      color: #333;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      margin-bottom: 20px;
    }
    table, th, td {
      border: 1px solid #aaa;
    }
    th, td {
      padding: 8px;
      text-align: left;
    }
    .assinatura {
      margin-top: 60px;
    }
  </style>
</head>
<body>

  <h1>Relatório Técnico de Obra</h1>

  <p>
    <strong>Engenheiro Responsável:</strong> {{nome_do_engenheiro}} – CREA {{numero do_CREA}} <br>
    <strong>Cliente:</strong> {{nome_do_cliente}} <br>
    <strong>Obra:</strong> {{nome_da_obra}}<br>
    <strong>Endereço:</strong> {{endereço}}<br>
    <strong>Período:</strong> {{data_inicial_do_periodo}} a {{data_final_do_periodo}}<br>
    <strong>Data do Relatório:</strong> {{data_do_relatorio}}
  </p>

  <h2>1. Objetivo</h2>
  <p>
    Este relatório tem como objetivo apresentar o resumo técnico das atividades executadas na obra durante o período especificado, bem como relatar eventuais ocorrências, condições climáticas e progresso das etapas.
  </p>

  <h2>2. Resumo das Atividades Executadas</h2>
  <table>
    <thead>
      <tr>
        <th>Data</th>
        <th>Atividades Realizadas</th>
        <th>Equipe/Observações</th>
      </tr>
    </thead>
    <tbody>
    {% for i in atividades %}
      <tr>
        <td>{{i.data_da_atividade}}</td>
        <td>{{i.atividade_realizada}}</td>
        <td>{{i.numero_de_pessoas_da_atividade}} {{i.funcao_das_pessoas_na_atividade}}, {{i.condicao_climatica_da_atividade}}</td>
      </tr>
    {% endfor %}
      <!-- Adicione mais linhas conforme necessário -->
    </tbody>
  </table>

  <h2>3. Condições Climáticas</h2>
  <p>
    Durante o período, as condições climáticas foram {{condições_climaticas}}, o que {{influenciou_nas_atividades}} a execução das etapas previstas.
  </p>

  <h2>4. Ocorrências Relevantes</h2>
  <ul>
    {% for i in ocorrencias %}
    <li>{{i.ocorrencia_relevante}} {{i.solução}}</li>
  </ul>

</body>
</html>
"""
        
    def get_POST_data(self, post):
        dados = {}

        # Campos fixos
        campos_simples = [
            'nome_do_engenheiro',
            'numero_do_CREA',
            'nome_do_cliente',
            'nome_da_obra',
            'endereço',
            'data_inicial_do_periodo',
            'data_final_do_periodo',
            'data_do_relatorio',
            'condicoes_climaticas',
            'influenciou_nas_atividades',
        ]

        for campo in campos_simples:
            dados[campo] = post.get(campo)

        # data_da_atividade pode ser múltipla
        dados['data_da_atividade'] = post.getlist('data_da_atividade')

        # Atividades
        atividades = []
        index = 0
        while True:
            prefixo = f'atividade_realizada[{index}]'
            num = post.get(f'{prefixo}[numero_de_pessoas_da_atividade]')
            func = post.get(f'{prefixo}[funcao_das_pessoas_na_atividade]')
            clima = post.get(f'{prefixo}[condicao_climatica_da_atividade]')

            if not any([num, func, clima]):
                break

            atividades.append({
                'numero_de_pessoas_da_atividade': num,
                'funcao_das_pessoas_na_atividade': func,
                'condicao_climatica_da_atividade': clima
            })
            index += 1

        dados['atividade_realizada'] = atividades

        # Ocorrências
        ocorrencias = []
        index = 0
        while True:
            prefixo = f'ocorrencias[{index}]'
            ocorr = post.get(f'{prefixo}[ocorrencia_relevante]')
            solucao = post.get(f'{prefixo}[solucao]')

            if not any([ocorr, solucao]):
                break

            ocorrencias.append({
                'ocorrencia_relevante': ocorr,
                'solucao': solucao
            })
            index += 1

        dados['ocorrencias'] = ocorrencias

        return dados          
    
    def get_json_response(self, text):
        linhas = text.strip().splitlines()

        comeco = None
        for i, linha in enumerate(linhas):
            if linha.strip().startswith("{") and comeco is None:
                comeco = i
            if linha.strip().endswith("}"):
                fim = i + 1

        if comeco is not None:
            json_puro = "\n".join(linhas[comeco:fim])
            return json_puro

        return None
    
    def gerar_relatorio(self, POSTobj):
        post = self.get_POST_data(POSTobj)
        exemplo_resposta = """
        {
        "nome_do_engenheiro": "Keven",
        "numero_do_CREA": "1234",
        "nome_do_cliente": "Lohan",
        "nome_da_obra": "Residência Unifamiliar",
        "endereco": "Rua Tatatata",
        "data_inicial_do_periodo": "2025-12-12",
        "data_final_do_periodo": "2026-12-12",
        "data_do_relatorio": "2025-07-13",
        "condicoes_climaticas": "predominantemente estáveis, com tempo seco",
        "influenciou_nas_atividades": "não impactaram de forma significativa",
        "atividades": [
            {
            "data_da_atividade": "2025-07-13",
            "atividade_realizada": "Execução de alvenaria de vedação",
            "numero_de_pessoas_da_atividade": "3",
            "funcao_das_pessoas_na_atividade": "profissionais alocados para o levantamento das paredes",
            "condicao_climatica_da_atividade": "tempo seco, favorável à atividade"
            },
            {
            "data_da_atividade": "2025-07-13",
            "atividade_realizada": "Aplicação de pintura em alvenaria",
            "numero_de_pessoas_da_atividade": "1",
            "funcao_das_pessoas_na_atividade": "pintor responsável pela aplicação da tinta",
            "condicao_climatica_da_atividade": "nível de umidade do ar ligeiramente elevado"
            }
        ],
        "ocorrencias": [
            {
            "ocorrencia_relevante": "Interrupção temporária da atividade de pintura devido a imprevistos com o profissional responsável",
            "solução": "Remarcação da atividade de pintura para o próximo dia útil, visando a otimização do cronograma"
            },
            {
            "ocorrencia_relevante": "Afastamento temporário de um dos pedreiros",
            "solucao": "Implementação de ajustes no planejamento, com consequente postergação do prazo de conclusão da alvenaria"
            }
        ]
        }
        """
        response = self.client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = f"""
            voce não pode alterar os dados, utilize apenas sinonimos com toms formais e jargões que substituem algo que ja foi dito.
            sua função é formatar e modular o texto de forma mais formal, digno de um relatorio de engenheiro civil.
            voce não acrescenta nem tira fatos, apenas enfeita eles e corrige erros ortograficos ou mudando a palavra por outras do mesmo sentido mas que aumentem a coerencia e coesão
            quero apenas a resposta do json, sem  comentarios extras apenas o json copiavel e colavel direto da sua resposta seguindo o exemplo de respose: {exemplo_resposta}, sem nada antes ou depois, apenas o json puro
            sabendo disso, voce deve formatar: {post} de forma que ele se encaixe perfeitamente com o documento de texto {self.exemplo_relatorio}
            as chaves serão a mesma do dicionario formatado
            se tiver mais de 3 campos com valor teste voce usara o exemplo de resposta que te enviei
            Retorne apenas o corpo JSON cru, sem nenhuma explicação ou chave externa. Só o conteúdo JSON puro
            """
        )
        json_response  = self.get_json_response(response.text)
        print(json_response)
        return RelatorioHandler(json_response).gerenete_html()
        
    def get_chat(self, chat_id):
        chat = Chat.objects.filter(id=chat_id).first()
        if chat is None:
            chat = Chat.objects.create(id=chat_id)
            chat.save()
        return chat
    
    def render_chat(self, chat):
        chat_rendered = chat.message_set.all()
        return chat_rendered
    
    def get_conversation(self, chat_rendered):
        temp = []
        for i in chat_rendered:
            temp.append(f"user: {i.requests}")
            temp.append(f"ia response: {i.responses}")
        return temp
        
    def make_ai_request(self, chat_id=0, current_data=""):
        chat = self.get_chat(chat_id)
        chat_rendered = self.render_chat(chat)
        chat_array = self.get_conversation(chat_rendered)
        chat_array.append(f'pergunta atual: {current_data}')
        
        response = self.client.models.generate_content(
        model="gemini-2.0-flash", contents=f"""essa parte entre parentese é apenas para leitura:
        (
        ignore user: e ia response: são apenas pra voce saber o autor das mensagens
        voce é um ia assistente de engenheros,
        o chat todo esta sendo compartilhado para facilitar o cache,
        a pergunta mais recente vai estar marcada no array como 'pergunta atual'
        ) {chat_array}"""
        )
        self.generate_relation_db(chat, current_data, response.text)
        if "gerar_relatorio" in response.text:
            data = response.text.split(';')
            print(data[1])
            
            c = RelatorioHandler(data[1])
            c.gerenete_html()
            
    def generate_relation_db(self, chat, requests, responses):
        msg_obj = Message(chat=chat, requests=requests, responses=responses)
        msg_obj.save()
        
import json
from django.template.loader import render_to_string
from .models import Relatorio
from django.http import HttpResponse

class RelatorioHandler:
    def __init__(self, json_data):
        self.json = json.loads(json_data)
    
    def gerenete_html(self):
        html = render_to_string('relatorio.html', self.json)
        return self.save_html(html)
    
    def save_html(self, html):
        relatorioobj = Relatorio(body=html)
        relatorioobj.save()
        return self.render_html(relatorioobj.id)
        
    def render_html(self, id=0):
        bodyobj = Relatorio.objects.filter(id=id).first()
        print(bodyobj)
        if bodyobj:
            return HttpResponse(bodyobj.body)