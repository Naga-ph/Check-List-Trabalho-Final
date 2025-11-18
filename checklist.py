import json
import os
from datetime import datetime, timedelta
import sys

# Declaração de Variáveis Globais

# A lista principal de tarefas, carregada do tarefas.json
TAREFAS = []

# Variável de controle para gerar IDs numéricos únicos
ID_CONTROLE = 0

# Constantes para as opções válidas
PRIORIDADES_VALIDAS = ["Urgente", "Alta", "Média", "Baixa"]
STATUS_VALIDOS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]
ORIGENS_VALIDAS = ["E-mail", "Telefone", "Chamado do Sistema"]

ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_ARQUIVADAS = "tarefas_arquivadas.json"

# Funções de Apoio (Validação, Persistência e Inicialização)

def inicializar_e_carregar_dados():
    """
    Função de inicialização do sistema.
    Verifica e cria arquivos JSON se não existirem[cite: 114, 119, 121, 122].
    Carrega a lista de tarefas do arquivo principal[cite: 104].
    Atualiza o ID_CONTROLE global[cite: 85].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função inicializar_e_carregar_dados")

    global TAREFAS
    global ID_CONTROLE

    # 1. Criação Automática de Arquivos Necessários [cite: 113, 119, 121]
    for arquivo in [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]:
        if not os.path.exists(arquivo):
            try:
                # Cria com estrutura inicial válida: lista vazia [] [cite: 121]
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=4)
                print(f"Arquivo '{arquivo}' criado com sucesso.")
            except IOError as e:
                print(f"Erro ao criar o arquivo {arquivo}: {e}")

    # 2. Carregamento do Arquivo Principal [cite: 104]
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            TAREFAS = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Em caso de erro ao ler ou decodificar, inicia com lista vazia
        TAREFAS = []

    # 3. Atualização do ID_CONTROLE [cite: 85]
    if TAREFAS:
        # Encontra o maior ID existente e incrementa para o próximo ID_CONTROLE
        max_id = max(tarefa.get('id', 0) for tarefa in TAREFAS)
        ID_CONTROLE = max_id + 1
    else:
        ID_CONTROLE = 1


def salvar_dados():
    """
    Salva a lista principal de tarefas no arquivo JSON[cite: 105, 106].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função salvar_dados")

    global TAREFAS
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            # default=str para formatar datetime
            json.dump(TAREFAS, f, indent=4, default=str)
        print(f"\nDados salvos em '{ARQUIVO_TAREFAS}' com sucesso.")
    except IOError as e:
        print(f"Erro ao salvar os dados no arquivo {ARQUIVO_TAREFAS}: {e}")


def buscar_tarefa_por_id(tarefa_id):
    """
    Busca uma tarefa na lista global pelo seu ID único.
    Parâmetros:
        tarefa_id (int): O ID da tarefa a ser buscada.
    Retorno:
        dict/None: A tarefa encontrada ou None se não for encontrada.
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função buscar_tarefa_por_id")

    for tarefa in TAREFAS:
        if tarefa['id'] == tarefa_id:
            return tarefa
    return None


def validar_opcao(prompt, opcoes_validas):
    """
    Valida a entrada do usuário contra uma lista de opções válidas (Case Insensitive).
    Parâmetros:
        prompt (str): A mensagem a ser exibida ao usuário.
        opcoes_validas (list): Lista de strings com as opções permitidas.
    Retorno:
        str: A opção escolhida pelo usuário em formato título, ou None em caso de erro.
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função validar_opcao")

    while True:
        try:
            entrada = input(f"{prompt} ({'/'.join(opcoes_validas)}): ").strip()
            if not entrada:
                print("Entrada não pode ser vazia.")
                continue

            # Validação Lógica [cite: 72, 73]
            for opcao in opcoes_validas:
                if entrada.lower() == opcao.lower():
                    return opcao  # Retorna a string original do conjunto de opções

            print(
                f"Opção inválida. Escolha uma das seguintes: {', '.join(opcoes_validas)}.")
        except Exception as e:
            # Tratamento de Exceções (Robustez Técnica) [cite: 76, 77]
            print(f"Ocorreu um erro na entrada: {e}. Tente novamente.")


def validar_id_tarefa(prompt):
    """
    Solicita e valida o ID de uma tarefa, garantindo que seja um número inteiro.
    Parâmetros:
        prompt (str): A mensagem a ser exibida ao usuário.
    Retorno:
        int/None: O ID válido ou None se a entrada for inválida.
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função validar_id_tarefa")

    while True:
        try:
            # Tratamento de Exceções para conversão de tipo (Robustez Técnica) [cite: 77]
            entrada = input(prompt).strip()
            if not entrada:
                return None
            tarefa_id = int(entrada)
            return tarefa_id
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro para o ID.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# ==============================================================================
# Funções do Ciclo de Vida da Tarefa (Encapsulamento e Modularização)
# ==============================================================================


def criar_tarefa():
    """
    Cria uma nova tarefa solicitando informações ao usuário[cite: 22, 23, 53].
    Valida os dados e adiciona a tarefa à lista global de tarefas[cite: 74].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função criar_tarefa")

    global TAREFAS
    global ID_CONTROLE

    print("\n--- Cadastro de Nova Tarefa ---")

    # Título (obrigatório) [cite: 15]
    titulo = input("Título (obrigatório, ex: Enviar Relatório): ").strip()
    if not titulo:
        print("Criação cancelada: Título é obrigatório.")
        return

    # Descrição (opcional) [cite: 15]
    descricao = input("Descrição (opcional): ").strip()

    # Prioridade (obrigatório) [cite: 16, 23]
    prioridade = validar_opcao("Prioridade (obrigatório)", PRIORIDADES_VALIDAS)
    if not prioridade:
        print("Criação cancelada: Prioridade é obrigatória.")
        return

    # Origem da Tarefa (obrigatório) [cite: 17, 23]
    origem = validar_opcao("Origem da Tarefa (obrigatório)", ORIGENS_VALIDAS)
    if not origem:
        print("Criação cancelada: Origem é obrigatória.")
        return

    # Criação da Tarefa
    nova_tarefa = {
        'id': ID_CONTROLE,  # ID Único [cite: 84]
        'titulo': titulo,
        'descricao': descricao,
        'prioridade': prioridade,
        'status': "Pendente",  # Status deve começar como "Pendente" [cite: 16]
        'origem': origem,
        # Data e Hora de Criação [cite: 18]
        'data_criacao': datetime.now().isoformat(),
        # Campo data_conclusao inicia como None [cite: 29]
        'data_conclusao': None
    }

    # Adiciona à lista global de tarefas (Edição de Variável Global) [cite: 63, 64]
    TAREFAS.append(nova_tarefa)

    # Incrementa o controle de ID para a próxima tarefa [cite: 85]
    ID_CONTROLE += 1

    print(f"\n✅ Tarefa '{titulo}' criada com sucesso! ID: {nova_tarefa['id']}")


def verificar_urgencia_e_pegar_tarefa():
    """
    Verifica se há tarefas com prioridade Urgente e a exibe,
    caso contrário, exibe a próxima prioridade disponível[cite: 24, 25, 26].
    Atualiza o status da tarefa selecionada para "Fazendo"[cite: 12, 27].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função verificar_urgencia_e_pegar_tarefa")

    tarefa_encontrada = None

    # Ordena as prioridades para verificar da mais alta para a mais baixa
    prioridades_ordenadas = ["Urgente", "Alta", "Média", "Baixa"]

    for prioridade_alvo in prioridades_ordenadas:
        for tarefa in TAREFAS:
            # Apenas tarefas Pendentes podem ser pegas
            if tarefa['status'] == "Pendente" and tarefa['prioridade'] == prioridade_alvo:
                tarefa_encontrada = tarefa
                break  # Encontrou a primeira da prioridade

        if tarefa_encontrada:
            break  # Sai do loop de prioridades se encontrou uma tarefa

    if tarefa_encontrada:
        # Atualiza o status para "Fazendo" [cite: 27]
        tarefa_encontrada['status'] = "Fazendo"

        print("\n--- Tarefa em Execução Selecionada ---")
        exibir_detalhes_tarefa(tarefa_encontrada)
        print(
            "\nStatus atualizado para 'Fazendo'. Lembre-se: Somente uma tarefa deve estar em execução por vez. [cite: 12]")
    else:
        print("\nNão há tarefas 'Pendente' para iniciar a execução.")


def atualizar_prioridade():
    """
    Permite ao usuário alterar a prioridade de uma tarefa existente[cite: 28].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função atualizar_prioridade")

    print("\n--- Atualizar Prioridade da Tarefa ---")

    tarefa_id = validar_id_tarefa(
        "Informe o ID da tarefa para atualizar a prioridade: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return

    tarefa = buscar_tarefa_por_id(tarefa_id)

    if not tarefa:
        print(f"Erro: Tarefa com ID {tarefa_id} não encontrada.")
        return

    print(
        f"Prioridade atual da tarefa '{tarefa['titulo']}' (ID: {tarefa_id}): {tarefa['prioridade']}")

    # Valida a nova prioridade [cite: 28]
    nova_prioridade = validar_opcao("Nova Prioridade", PRIORIDADES_VALIDAS)

    if nova_prioridade:
        tarefa['prioridade'] = nova_prioridade
        print(
            f"\n✅ Prioridade da tarefa {tarefa_id} atualizada para '{nova_prioridade}'.")
    else:
        print("Atualização de prioridade cancelada ou inválida.")


def concluir_tarefa():
    """
    Conclui uma tarefa, atualizando seu status e registrando a data de conclusão[cite: 29, 31].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função concluir_tarefa")

    print("\n--- Concluir Tarefa ---")

    tarefa_id = validar_id_tarefa(
        "Informe o ID da tarefa que deseja concluir: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return

    tarefa = buscar_tarefa_por_id(tarefa_id)

    if not tarefa:
        print(f"Erro: Tarefa com ID {tarefa_id} não encontrada.")
        return

    if tarefa['status'] == "Concluída":
        print(
            f"A tarefa {tarefa_id} já está concluída desde {tarefa['data_conclusao']}.")
        return

    # Adiciona a data de conclusão (tipo de dado apropriado) [cite: 29]
    tarefa['data_conclusao'] = datetime.now().isoformat()

    # Altera o status para "Concluída" [cite: 31]
    tarefa['status'] = "Concluída"

    print(
        f"\n✅ Tarefa '{tarefa['titulo']}' (ID: {tarefa_id}) concluída com sucesso!")
    print(f"Data de Conclusão registrada: {tarefa['data_conclusao']}")


def exclusao_logica():
    """
    Realiza a exclusão lógica de uma tarefa, mudando seu status para "Excluída"[cite: 33].
    A tarefa não é removida da lista principal[cite: 33].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função exclusao_logica")

    print("\n--- Exclusão Lógica de Tarefa ---")

    tarefa_id = validar_id_tarefa(
        "Informe o ID da tarefa para exclusão lógica: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return

    tarefa = buscar_tarefa_por_id(tarefa_id)

    if not tarefa:
        print(f"Erro: Tarefa com ID {tarefa_id} não encontrada.")
        return

    if tarefa['status'] == "Excluída":
        print(f"A tarefa {tarefa_id} já está marcada como 'Excluída'.")
        return

    # Atualiza o status para "Excluída" [cite: 33]
    tarefa['status'] = "Excluída"

    print(
        f"\n✅ Tarefa '{tarefa['titulo']}' (ID: {tarefa_id}) marcada como 'Excluída' (Exclusão Lógica).")


def arquivar_tarefas_antigas():
    """
    Move tarefas concluídas há mais de uma semana para o arquivo de arquivadas[cite: 32, 108, 110].
    Atualiza o status para "Arquivado" na lista principal[cite: 32].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função arquivar_tarefas_antigas")

    global TAREFAS
    tarefas_para_arquivar = []
    lista_principal_atualizada = []
    limite_data = datetime.now() - timedelta(weeks=1)

    # 1. Identificar tarefas para arquivar [cite: 32]
    for tarefa in TAREFAS:
        if tarefa['status'] == "Concluída" and tarefa.get('data_conclusao'):
            try:
                # Converte string de data para objeto datetime
                data_conclusao = datetime.fromisoformat(
                    tarefa['data_conclusao'])

                # Tarefas concluídas com mais de uma semana [cite: 32]
                if data_conclusao < limite_data:
                    # Atualiza status [cite: 32]
                    tarefa['status'] = "Arquivado"
                    tarefas_para_arquivar.append(tarefa)
                    continue  # Não adiciona à lista_principal_atualizada neste momento
            except ValueError:
                # Em caso de erro de conversão de data, mantém na lista principal e pula
                lista_principal_atualizada.append(tarefa)
                continue

        # Tarefas com status "Excluída" também são candidatas ao arquivamento/limpeza,
        # mas a regra principal é sobre "Concluída há mais de uma semana"[cite: 108].
        # Aqui, vamos focar na regra de tempo.

        # Mantém as tarefas que não serão arquivadas por tempo na lista ativa
        if tarefa['status'] != "Arquivado":
            lista_principal_atualizada.append(tarefa)

    # 2. Persistir no arquivo de arquivadas [cite: 110, 111]
    if tarefas_para_arquivar:
        print(
            f"\n📢 Iniciando arquivamento automático de {len(tarefas_para_arquivar)} tarefa(s) antiga(s)...")

        # Carrega o histórico de arquivadas para acumular [cite: 111]
        historico_arquivadas = []
        try:
            with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
                historico_arquivadas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            historico_arquivadas = []

        # Adiciona as novas tarefas arquivadas
        historico_arquivadas.extend(tarefas_para_arquivar)

        # Salva o arquivo de histórico
        try:
            with open(ARQUIVO_ARQUIVADAS, 'w', encoding='utf-8') as f:
                # default=str para garantir que a data seja serializada corretamente
                json.dump(historico_arquivadas, f, indent=4, default=str)
            print(
                f"✅ {len(tarefas_para_arquivar)} tarefa(s) registrada(s) em '{ARQUIVO_ARQUIVADAS}'.")
        except IOError as e:
            print(f"Erro ao salvar arquivo de arquivadas: {e}")

    # 3. Atualiza a lista principal de tarefas
    # A lista_principal_atualizada já contém as tarefas que DEVEM permanecer ativas.
    # As tarefas arquivadas por tempo ou logicamente excluídas foram movidas
    # para 'tarefas_arquivadas.json' e removidas da lista TAREFAS (limpeza).

    # Reatribui a lista global [cite: 63, 64]
    TAREFAS = lista_principal_atualizada

    if tarefas_para_arquivar:
        print("Lista ativa de tarefas limpa e organizada.")
    else:
        print("\nNenhuma tarefa concluída há mais de uma semana para arquivar.")


def calcular_tempo_execucao(data_criacao_str, data_conclusao_str):
    """
    Calcula o tempo de execução de uma tarefa a partir das strings de data e hora.
    Parâmetros:
        data_criacao_str (str): Data e hora de criação no formato ISO.
        data_conclusao_str (str): Data e hora de conclusão no formato ISO.
    Retorno:
        str: O tempo de execução formatado (dias, horas, minutos), ou None em caso de erro.
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função calcular_tempo_execucao")

    try:
        data_criacao = datetime.fromisoformat(data_criacao_str)
        data_conclusao = datetime.fromisoformat(data_conclusao_str)

        tempo_total = data_conclusao - data_criacao

        total_segundos = int(tempo_total.total_seconds())
        dias = total_segundos // 86400
        horas = (total_segundos % 86400) // 3600
        minutos = (total_segundos % 3600) // 60

        return f"{dias} dias, {horas} horas, {minutos} minutos"
    except ValueError:
        return "Erro no formato de data"
    except Exception as e:
        return f"Erro ao calcular tempo: {e}"


def exibir_detalhes_tarefa(tarefa):
    """
    Exibe os detalhes de uma tarefa, incluindo o cálculo do tempo se concluída[cite: 34, 35].
    Parâmetros:
        tarefa (dict): O dicionário da tarefa.
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função exibir_detalhes_tarefa")

    print("-" * 50)
    print(f"ID: {tarefa.get('id', 'N/A')}")
    print(f"Título: {tarefa.get('titulo', 'N/A')}")
    print(f"Descrição: {tarefa.get('descricao', 'N/A')}")
    print(f"Prioridade: {tarefa.get('prioridade', 'N/A')}")
    print(f"Status: {tarefa.get('status', 'N/A')}")
    print(f"Origem: {tarefa.get('origem', 'N/A')}")
    print(f"Data de Criação: {tarefa.get('data_criacao', 'N/A')}")

    data_conc = tarefa.get('data_conclusao')
    if data_conc:
        print(f"Data de Conclusão: {data_conc}")

        # Calcular o tempo de execução da tarefa [cite: 35]
        tempo_execucao = calcular_tempo_execucao(
            tarefa['data_criacao'], data_conc)
        print(f"Tempo de Execução: {tempo_execucao}")
    print("-" * 50)


def relatorio_tarefas_ativas():
    """
    Exibe todas as informações da tarefa na tela (apenas ativas)[cite: 34].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função relatorio_tarefas_ativas")

    print("\n==================================================")
    print("        RELATÓRIO DE TAREFAS ATIVAS               ")
    print("==================================================")

    tarefas_ativas = [t for t in TAREFAS if t['status']
                      not in ["Arquivado", "Excluída"]]

    if not tarefas_ativas:
        print("Nenhuma tarefa ativa para exibir.")
        return

    # Ordena por Prioridade (Urgente, Alta, Média, Baixa) e depois por ID
    def chave_ordenacao(tarefa):
        try:
            prioridade_idx = PRIORIDADES_VALIDAS.index(
                tarefa.get('prioridade', 'Baixa'))
        except ValueError:
            # Coloca inválidas no fim
            prioridade_idx = len(PRIORIDADES_VALIDAS)
        return (prioridade_idx, tarefa.get('id', float('inf')))

    tarefas_ordenadas = sorted(tarefas_ativas, key=chave_ordenacao)

    for tarefa in tarefas_ordenadas:
        exibir_detalhes_tarefa(tarefa)


def relatorio_tarefas_arquivadas():
    """
    Exibe a lista de tarefas arquivadas, lendo do arquivo JSON[cite: 36, 37].
    Tarefas excluídas não devem ser listadas[cite: 37].
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print(
        # Prints de Execução [cite: 80, 81]
        "Executando a função relatorio_tarefas_arquivadas")

    print("\n==================================================")
    print("        RELATÓRIO DE TAREFAS ARQUIVADAS           ")
    print("==================================================")

    try:
        with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
            tarefas_arquivadas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tarefas_arquivadas = []

    # Filtra tarefas excluídas (Excluídas não devem ser listadas) [cite: 37]
    tarefas_para_exibir = [
        t for t in tarefas_arquivadas if t.get('status') != "Excluída"]

    if not tarefas_para_exibir:
        print(
            f"Nenhuma tarefa encontrada no arquivo '{ARQUIVO_ARQUIVADAS}' ou todas são 'Excluídas'.")
        return

    for tarefa in tarefas_para_exibir:
        exibir_detalhes_tarefa(tarefa)

# ==============================================================================
# Menu Principal (Abstração de Controle) [cite: 42, 43, 71]
# ==============================================================================


def exibir_menu():
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 50)
    print("         💻 Gerenciamento de Tarefas v1.0         ")
    print("=" * 50)
    print("1. Criar Nova Tarefa")
    print("2. Pegar Próxima Tarefa (Verificar Urgência)")
    print("3. Atualizar Prioridade de Tarefa")
    print("4. Concluir Tarefa")
    print("5. Exclusão Lógica de Tarefa")
    print("6. Executar Limpeza e Arquivamento Automático")
    print("7. Relatório de Tarefas Ativas")
    print("8. Relatório de Tarefas Arquivadas")
    print("9. Sair do Programa")
    print("=" * 50)


def main():
    """
    Corpo principal do programa, responsável pelo fluxo de execução e menu.
    """
    # 1. Inicializa e carrega os dados
    inicializar_e_carregar_dados()

    while True:
        exibir_menu()

        # Tratamento de Exceções para entrada de menu (Robustez Técnica) [cite: 77]
        try:
            # Validação da opção (Validação Lógica) [cite: 46]
            opcao_str = input("Escolha uma opção: ").strip()

            if not opcao_str.isdigit():
                print("\n⚠️ Opção inválida. Por favor, digite o número da opção.")
                continue

            opcao = int(opcao_str)
        except Exception:
            print("\n⚠️ Entrada inválida. Tente novamente com um número.")
            continue

        # 2. Executa a função da opção escolhida [cite: 48]
        if opcao == 1:
            criar_tarefa()
        elif opcao == 2:
            verificar_urgencia_e_pegar_tarefa()
        elif opcao == 3:
            atualizar_prioridade()
        elif opcao == 4:
            concluir_tarefa()
        elif opcao == 5:
            exclusao_logica()
        elif opcao == 6:
            arquivar_tarefas_antigas()
        elif opcao == 7:
            relatorio_tarefas_ativas()
        elif opcao == 8:
            relatorio_tarefas_arquivadas()
        elif opcao == 9:
            print("\nFinalizando o programa...")
            # Salva os dados antes de finalizar o programa [cite: 105]
            salvar_dados()
            # Encerra o programa [cite: 106]
            sys.exit(0)
        else:
            # Validação: Opção deve existir [cite: 46]
            print(
                "\n⚠️ Opção não existe no menu. Por favor, escolha uma opção válida (1-9).")


if __name__ == "__main__":
    main()
