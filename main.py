import streamlit as st
from apps import selecvars, selecinds,operationsbuy,operationssell

estrategias = ["Cruzamento de Médias", "Bandas de Bollinger", "VWAP", "IFR", "OBV","Canais de Keltner","HiLo Activator","MACD","Estocastico","Stop ATR","Parabolic SAR"]
floats_select_dict = {"Cruzamento de Médias":"vMedia1,vMedia2", "Bandas de Bollinger": "vBollinger1,vBollinger2", "VWAP":"vVWAP", 
                      "IFR":"vIFR","OBV":"vOBV","Canais de Keltner":"vKeltnerCH1,vKeltnerCH2","HiLo Activator":"vHiloActivator",
                      "MACD":"vMACD,vMACDEXP","Estocastico":"vFullStochastic","Stop ATR":"vStopATR","Parabolic SAR":"vParabolicSAR"}  

# Inicializa os estados, se necessário
if 'create_clicked' not in st.session_state:
    st.session_state.create_clicked = False
if 'next_clicked' not in st.session_state:
    st.session_state.next_clicked = False
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []
if 'gerar_button_enabled' not in st.session_state:
    st.session_state.gerar_button_enabled = False  # Inicialmente desabilitado
if 'gerar_clicked' not in st.session_state:
    st.session_state.gerar_clicked = False  # Controla quando o botão "Gerar" foi clicado
if 'install_clicked' not in st.session_state:
    st.session_state.install_clicked = False

st.sidebar.html("""
    <style>
    .stSidebar{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .stSidebar button {
        width: 100%;
    }
    </style>
    """)

create = st.sidebar.button("Crie o seu robô")
install = st.sidebar.button("Como utilizar?")
infos = st.sidebar.button("Saiba mais do desenvolvedor")

if create:
    st.session_state.create_clicked = True
    st.session_state.next_clicked = False  # Reset 'Next' button state
    st.session_state.selected_options = []  # Reset selected options
    st.session_state.gerar_button_enabled = False  # Desabilita o botão "Gerar"
    st.session_state.gerar_clicked = False  # Reseta o estado de clique do botão "Gerar"
    st.session_state.install_clicked = False

if install:
    st.session_state.install_clicked = True
    st.session_state.create_clicked = False
    st.session_state.next_clicked = False  # Reset 'Next' button state
    st.session_state.selected_options = []  # Reset selected options
    st.session_state.gerar_button_enabled = False  # Desabilita o botão "Gerar"
    st.session_state.gerar_clicked = False  # Reseta o estado de clique do botão "Gerar"
    

if infos:
    st.write("Tu não precisa saber disso")

if st.session_state.install_clicked:
    st.image("htu1.png",caption="Preencha os campos")
    st.image("htu2.png",caption="Clique em gerar")
    st.image("htu3.png",caption="Copie o código")
    st.image("htu4.png",caption="Formate e execute!")
# Exibe o multiselect se 'create' foi clicado
if st.session_state.create_clicked:
    # Limita a seleção de até 5 indicadores de entrada
    options = st.multiselect(
        "Selecione os indicadores de entrada",
        estrategias,
        max_selections=5  # Limita a seleção a 5 opções
    )

    # Armazena as opções selecionadas no estado
    st.session_state.selected_options = options
   

    if options:
        
        next_button = st.button("Next")

        if next_button or st.session_state.next_clicked:
            st.session_state.next_clicked = True  # Mantém o estado do botão "Next" clicado
            all_inputs_filled = True  # Flag para verificar se todos os inputs foram preenchidos
            var = []
            indicatos = []
            buy_strategies = []
            sell_strategies = []
            exit_buy_strategies = []
            exit_sell_strategies = []
            vpac= ""
            for option in st.session_state.selected_options:

                #INDICADOR CRUZAMENTO DE MEDIA MOVEL

                if option == estrategias[0]:
                    st.title(f"{option}")
                    mm1_periodo = st.number_input("", value=None, placeholder="Selecione o período da média móvel rápida", step=1, format="%d")
                    mm2_periodo = st.number_input("", value=None, placeholder="Selecione o período da média móvel lenta", step=1, format="%d")
                    mm_var = f"{floats_select_dict[option]}: float;"
                    var.append(mm_var)
                    mm1_ind = f"vMedia1 := Media({mm1_periodo},Close);" 
                    mm2_ind = f"vMedia2 := Media({mm2_periodo},Close);"
                    mm_strategy_sell = "(vMedia1[1] > vMedia2[1]) and (vMedia1 < vMedia2)"
                    mm_strategy_buy = "(vMedia1[1] < vMedia2[1]) and (vMedia1 > vMedia2)"
                    mm_exit = st.selectbox("Selecione o tipo de posição das médias",("Entrada", "Saída", "Entrada/Saída"))
                    mm_side = st.selectbox("Selecione o tipo de estratégia das médias",("Compra", "Venda", "Ambos"))
                    mm_invert = st.selectbox("Operar Invertido?",("Não", "Sim"))
                    mm_invert = True if mm_invert == "Sim" else False
                    if mm_invert:
                       mm_strategy_sell = "(vMedia1[1] < vMedia2[1]) and (vMedia1 > vMedia2)"
                       mm_strategy_buy = "(vMedia1[1] > vMedia2[1]) and (vMedia1 < vMedia2)"
                    if mm_side == "Compra":
                        if mm_exit == "Saída":
                            exit_buy_strategies.append(mm_strategy_buy)
                        elif mm_exit == "Entrada":
                            buy_strategies.append(mm_strategy_buy)
                        elif mm_exit == "Entrada/Saída":
                            exit_buy_strategies.append(mm_strategy_buy)
                            buy_strategies.append(mm_strategy_buy)
                    elif mm_side == "Venda":
                        if mm_exit == "Saída":
                            exit_sell_strategies.append(mm_strategy_sell)
                        elif mm_exit == "Entrada":
                            sell_strategies.append(mm_strategy_sell)
                        elif mm_exit == "Entrada/Saída":
                            exit_sell_strategies.append(mm_strategy_sell)
                            sell_strategies.append(mm_strategy_sell)     
                    elif mm_side == "Ambos":
                        if mm_exit == "Saída":
                            exit_sell_strategies.append(mm_strategy_sell)
                            exit_buy_strategies.append(mm_strategy_buy)
                        elif mm_exit == "Entrada":
                            buy_strategies.append(mm_strategy_buy)
                            sell_strategies.append(mm_strategy_sell)
                        elif mm_exit == "Entrada/Saída":
                            exit_buy_strategies.append(mm_strategy_buy)
                            buy_strategies.append(mm_strategy_buy)
                            exit_sell_strategies.append(mm_strategy_sell)
                            sell_strategies.append(mm_strategy_sell)
                    indicatos.append(mm1_ind)
                    indicatos.append(mm2_ind)

                    if mm1_periodo is None or mm2_periodo is None or mm_side is None or mm_invert is None or mm_exit is None:
                        all_inputs_filled = False


                    #indicador de BB

                elif option == estrategias[1]:
                    st.title(f"{option}")
                    bb_desv = st.number_input("", value=None, placeholder="Selecione o período do desvio padrão", step=1, format="%d")
                    bb_periodo = st.number_input("", value=None, placeholder="Selecione o período da média", step=1, format="%d")
                    bb_side = st.selectbox("Selecione o tipo de estratégia das Bandas", ("Compra", "Venda", "Ambos"))
                    bb_exit = st.selectbox("Selecione o tipo de posição das Bandas",("Entrada", "Saída", "Entrada/Saída"))
                    bb_invert = st.selectbox("Operar Invertido com as Bandas?", ("Não", "Sim"))
                    st.write("FFD = Fechou Fora Dentro")
                    st.write("FFD = Fechou Fora Dentro")
                    st.write("FFDF = Fechou Fora Dentro e Fora")
                    bb_estrategia = st.selectbox("Selecione o tipo de estratégia", ("FF", "FFD", "FFDF"))
                    bb_var = f"{floats_select_dict[option]}: float;"
                    var.append(bb_var)
                    bb_ind1 = f"vBollinger1:= BollingerBands({bb_desv},{bb_periodo},0)|0|;"
                    bb_ind2 = f"vBollinger2:= BollingerBands({bb_desv},{bb_periodo},0)|1|;"
                    
                    if bb_estrategia == "FF":
                        bb_strategy_sell = "(Close > vBollinger1)"
                        bb_strategy_buy = "(Close < vBollinger2)"
                    elif bb_estrategia == "FFD":
                        bb_strategy_sell = "(Close[1] > vBollinger1[1]) and (Close < vBollinger1)"
                        bb_strategy_buy = "(Close[1] < vBollinger2[1]) and (Close > vBollinger2)"
                    elif bb_estrategia == "FFDF":
                        bb_strategy_sell = "(Close[2] > vBollinger1[2]) and (Close[1] < vBollinger1[1]) and (Close > vBollinger1)"
                        bb_strategy_buy = "(Close[2] < vBollinger2[2]) and (Close[1] > vBollinger2[1]) and (Close > vBollinger2)"
                    
                    bb_invert = True if bb_invert == "Sim" else False
                    if bb_invert:
                       bb_strategy_sell = bb_strategy_sell.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                       bb_strategy_buy = bb_strategy_buy.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                    if bb_side == "Compra":
                        if bb_exit == "Saída":
                            exit_buy_strategies.append(bb_strategy_buy)
                        elif bb_exit == "Entrada":
                            buy_strategies.append(bb_strategy_buy)
                        elif bb_exit == "Entrada/Saída":
                            exit_buy_strategies.append(bb_strategy_buy)
                            buy_strategies.append(bb_strategy_buy)
                    elif bb_side == "Venda":
                        if bb_exit == "Saída":
                            exit_sell_strategies.append(bb_strategy_sell)
                        elif bb_exit == "Entrada":
                            sell_strategies.append(bb_strategy_sell)
                        elif bb_exit == "Entrada/Saída":
                            exit_sell_strategies.append(bb_strategy_sell)
                            sell_strategies.append(bb_strategy_sell)     
                    elif bb_side == "Ambos":
                        if bb_exit == "Saída":
                            exit_sell_strategies.append(bb_strategy_sell)
                            exit_buy_strategies.append(bb_strategy_buy)
                        elif bb_exit == "Entrada":
                            buy_strategies.append(bb_strategy_buy)
                            sell_strategies.append(bb_strategy_sell)
                        elif bb_exit == "Entrada/Saída":
                            exit_buy_strategies.append(bb_strategy_buy)
                            buy_strategies.append(bb_strategy_buy)
                            exit_sell_strategies.append(bb_strategy_sell)
                            sell_strategies.append(bb_strategy_sell)
                    indicatos.append(bb_ind1)
                    indicatos.append(bb_ind2)

                    

                    if bb_desv is None or bb_periodo is None or bb_side is None or bb_invert is None or bb_estrategia is None:
                        all_inputs_filled = False


                        ##INDICADOR DE VWAP

                elif option == estrategias[2]:
                    st.title(f"{option}")
                    vwap_periodo = st.number_input("", value=None, placeholder="Selecione o período da VWAP", step=1, format="%d")
                    vwap_estrategia = st.selectbox("Selecione o tipo de filtro para VWAP",("Acima", "Abaixo"),)
                    vwap_var = f"{floats_select_dict[option]}: float;"
                    var.append(vwap_var)
                    vwap_ind = f"{floats_select_dict[option]} := VWAP({vwap_periodo});"
                    if vwap_estrategia == "Acima":
                        vwap_strategy_sell = f"(Close > {floats_select_dict[option]})"
                        sell_strategies.append(vwap_strategy_sell)
                    elif vwap_estrategia == "Abaixo":
                        vwap_strategy_buy = f"(Close < {floats_select_dict[option]})" 
                        buy_strategies.append(vwap_strategy_buy)
                    indicatos.append(vwap_ind)

                    if vwap_periodo is None or vwap_estrategia is None:
                        all_inputs_filled = False


                        #INDICADOR ifr

                elif option == estrategias[3]:
                    st.title(f"{option}")
                    ifr_periodo = st.number_input("", value=None, placeholder="Selecione o período de IFR", step=1, format="%d")
                    ifr_superior= st.number_input("", value=None, placeholder="Selecione o valor superior", step=1, format="%d")
                    ifr_inferior= st.number_input("", value=None, placeholder="Selecione o valor inferior", step=1, format="%d")
                    ifr_side = st.selectbox("Selecione o tipo de estratégia de IFR",("Compra", "Venda","Ambos"),)
                    ifr_exit = st.selectbox("Selecione o tipo de posição do IFR",("Entrada", "Saída", "Entrada/Saída"))
                    ifr_invert = st.selectbox("Operar Invertido com o IFR?",("Não", "Sim"),)
                    ifr_var = f"{floats_select_dict[option]}: float;"
                    var.append(ifr_var)
                    ifr_ind = f"{floats_select_dict[option]} := IFR({ifr_periodo});"
                    ifr_strategy_buy = f"(vIFR < {ifr_inferior})"
                    ifr_strategy_sell = f"(vIFR > {ifr_superior})"
                    ifr_invert = True if ifr_invert == "Sim" else False 
                    if ifr_invert:
                        ifr_strategy_sell = ifr_strategy_sell.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                        ifr_strategy_buy = ifr_strategy_buy.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                    if ifr_side == "Compra":
                        if ifr_exit == "Saída":
                            exit_buy_strategies.append(ifr_strategy_buy)
                        elif ifr_exit == "Entrada":
                            buy_strategies.append(ifr_strategy_buy)
                        elif ifr_exit == "Entrada/Saída":
                            exit_buy_strategies.append(ifr_strategy_buy)
                            buy_strategies.append(ifr_strategy_buy)
                    elif ifr_side == "Venda":
                        if ifr_exit == "Saída":
                            exit_sell_strategies.append(ifr_strategy_sell)
                        elif ifr_exit == "Entrada":
                            sell_strategies.append(ifr_strategy_sell)
                        elif ifr_exit == "Entrada/Saída":
                            exit_sell_strategies.append(ifr_strategy_sell)
                            sell_strategies.append(ifr_strategy_sell)     
                    elif ifr_side == "Ambos":
                        if ifr_exit == "Saída":
                            exit_sell_strategies.append(ifr_strategy_sell)
                            exit_buy_strategies.append(ifr_strategy_buy)
                        elif ifr_exit == "Entrada":
                            buy_strategies.append(ifr_strategy_buy)
                            sell_strategies.append(ifr_strategy_sell)
                        elif ifr_exit == "Entrada/Saída":
                            exit_buy_strategies.append(ifr_strategy_buy)
                            buy_strategies.append(ifr_strategy_buy)
                            exit_sell_strategies.append(ifr_strategy_sell)
                            sell_strategies.append(ifr_strategy_sell)
                    indicatos.append(ifr_ind)
                    if ifr_periodo is None or ifr_superior is None or ifr_inferior is None or ifr_side is None or ifr_invert is None:
                        all_inputs_filled = False


                #INDICADOR OBV

                elif option == estrategias[4]:
                    st.title(f"{option}")
                    obv_entrada = st.number_input("", value=None, placeholder="Selecione o valor de OBV", step=1, format="%d")
                    obv_invert = st.selectbox("Operar Invertido com o OBV?",("Não", "Sim"),)
                    obv_side = st.selectbox("Selecione o tipo de estratégia de OBV",("Compra", "Venda","Ambos"),)
                    obv_exit = st.selectbox("Selecione o tipo de posição do OBV",("Entrada", "Saída", "Entrada/Saída"))
                    obv_var = f"{floats_select_dict[option]}: float;"
                    obv_var1 = f"vOBVmed: float;"
                    var.append(obv_var)
                    var.append(obv_var1)
                    obv_ind = f"{floats_select_dict[option]} := OBV;"
                    obv_ind2 = f"vOBVmed := Media({obv_entrada},vOBV);"
                    obv_strategy_buy = f"(vOBV[1] < vOBVmed[1]) and (vOBV > vOBVmed)"
                    obv_strategy_sell = f"(vOBV[1] > vOBVmed[1]) and (vOBV < vOBVmed)"
                    obv_invert = True if obv_invert == "Sim" else False 
                    if obv_invert:
                        obv_strategy_sell = obv_strategy_sell.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                        obv_strategy_buy = obv_strategy_buy.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<") 
                    if obv_side == "Compra":
                        if obv_exit == "Saída":
                            exit_buy_strategies.append(obv_strategy_buy)
                        elif obv_exit == "Entrada":
                            buy_strategies.append(obv_strategy_buy)
                        elif obv_exit == "Entrada/Saída":
                            exit_buy_strategies.append(obv_strategy_buy)
                            buy_strategies.append(obv_strategy_buy)
                    elif obv_side == "Venda":
                        if obv_exit == "Saída":
                            exit_sell_strategies.append(obv_strategy_sell)
                        elif obv_exit == "Entrada":
                            sell_strategies.append(obv_strategy_sell)
                        elif obv_exit == "Entrada/Saída":
                            exit_sell_strategies.append(obv_strategy_sell)
                            sell_strategies.append(obv_strategy_sell)     
                    elif obv_side == "Ambos":
                        if obv_exit == "Saída":
                            exit_sell_strategies.append(obv_strategy_sell)
                            exit_buy_strategies.append(obv_strategy_buy)
                        elif obv_exit == "Entrada":
                            buy_strategies.append(obv_strategy_buy)
                            sell_strategies.append(obv_strategy_sell)
                        elif obv_exit == "Entrada/Saída":
                            exit_buy_strategies.append(obv_strategy_buy)
                            buy_strategies.append(obv_strategy_buy)
                            exit_sell_strategies.append(obv_strategy_sell)
                            sell_strategies.append(obv_strategy_sell)
                    indicatos.append(obv_ind)
                    indicatos.append(obv_ind2)

                    if obv_entrada is None or obv_invert is None or obv_side is None:
                        all_inputs_filled = False

                #INDICADOR keltner

                elif option == estrategias[5]:
                    st.title(f"{option}")
                    keltner_desv = st.number_input("", value=None, placeholder="Selecione o período do desvio padrão de Keltner", step=1, format="%d")
                    keltner_periodo = st.number_input("", value=None, placeholder="Selecione o período dos canais de Keltner", step=1, format="%d")
                    keltner_side = st.selectbox("Selecione o tipo de estratégia dos Canais",("Compra", "Venda","Ambos"),)
                    keltner_exit = st.selectbox("Selecione o tipo de posição do Keltner",("Entrada", "Saída", "Entrada/Saída"))
                    keltner_invert = st.selectbox("Operar Invertido com os canais de keltner?",("Não", "Sim"),)
                    st.write("FFD = Fechou Fora Dentro")
                    st.write("FFD = Fechou Fora Dentro")
                    st.write("FFDF = Fechou Fora Dentro e Fora")
                    keltner_estrategia = st.selectbox("Selecione o tipo de estratégia de Keltner",("FF", "FFD","FFDF"),)
                    keltner_var = f"{floats_select_dict[option]}: float;"
                    var.append(keltner_var)
                    keltner_ind1 = f"vKeltnerCH1:= KeltnerCH({keltner_desv},{keltner_periodo},0)|0|;"
                    keltner_ind2 = f"vKeltnerCH2:= KeltnerCH({keltner_desv},{keltner_periodo},0)|1|;"
                    ##FAZER A LOGICA DE COMPRA DO BB
                    if keltner_estrategia == "FF":
                        keltner_strategy_sell = ("(Close > vKeltnerCH1)")
                        keltner_strategy_buy = ("(Close < vKeltnerCH2)")
                    elif keltner_estrategia == "FFD":
                        keltner_strategy_sell = ("(Close[1] > vKeltnerCH1[1]) and (Close < vKeltnerCH1)")
                        keltner_strategy_buy = ("(Close[1] < vKeltnerCH2[1]) and (Close > vKeltnerCH2)")
                    elif keltner_estrategia == "FFDF":
                        keltner_strategy_sell = ("(Close[2] > vKeltnerCH1[2]) and (Close[1] < vKeltnerCH1[1]) and (Close > vKeltnerCH1)")
                        keltner_strategy_buy = ("(Close[2] < vKeltnerCH2[2]) and (Close[1] > vKeltnerCH2[1]) and (Close > vKeltnerCH2)")
                    keltner_invert = True if keltner_invert == "Sim" else False
                    if keltner_invert:
                       keltner_strategy_sell = keltner_strategy_sell.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                       keltner_strategy_buy = keltner_strategy_buy.replace(">", "TEMP").replace("<", ">").replace("TEMP", "<")
                    if keltner_side == "Compra":
                        if keltner_exit == "Saída":
                            exit_buy_strategies.append(keltner_strategy_buy)
                        elif keltner_exit == "Entrada":
                            buy_strategies.append(keltner_strategy_buy)
                        elif keltner_exit == "Entrada/Saída":
                            exit_buy_strategies.append(keltner_strategy_buy)
                            buy_strategies.append(keltner_strategy_buy)
                    elif keltner_side == "Venda":
                        if keltner_exit == "Saída":
                            exit_sell_strategies.append(keltner_strategy_sell)
                        elif keltner_exit == "Entrada":
                            sell_strategies.append(keltner_strategy_sell)
                        elif keltner_exit == "Entrada/Saída":
                            exit_sell_strategies.append(keltner_strategy_sell)
                            sell_strategies.append(keltner_strategy_sell)     
                    elif keltner_side == "Ambos":
                        if keltner_exit == "Saída":
                            exit_sell_strategies.append(keltner_strategy_sell)
                            exit_buy_strategies.append(keltner_strategy_buy)
                        elif keltner_exit == "Entrada":
                            buy_strategies.append(keltner_strategy_buy)
                            sell_strategies.append(keltner_strategy_sell)
                        elif keltner_exit == "Entrada/Saída":
                            exit_buy_strategies.append(keltner_strategy_buy)
                            buy_strategies.append(keltner_strategy_buy)
                            exit_sell_strategies.append(keltner_strategy_sell)
                            sell_strategies.append(keltner_strategy_sell)
                    indicatos.append(keltner_ind1)
                    indicatos.append(keltner_ind2)

                    if keltner_desv is None or keltner_periodo is None or keltner_side is None or keltner_invert is None or keltner_estrategia is None:
                        all_inputs_filled = False

                    #INDICADOR HiLo Activator

                elif option == estrategias[6]:
                    st.title(f"{option}")
                    hilo_periodo = st.number_input("", value=None, placeholder="Selecione o período do HiLo", step=1, format="%d")
                    hilo_side = st.selectbox("Selecione o tipo de estratégia do HiLo",("Compra", "Venda","Ambos"))
                    hilo_exit = st.selectbox("Selecione o tipo de posição do HiLo",("Entrada", "Saída", "Entrada/Saída"))
                    hilo_invert = st.selectbox("Operar Invertido com HiLo?",("Não", "Sim"),)
                    hilo_var = f"{floats_select_dict[option]}: integer;"
                    var.append(hilo_var)
                    hilo_ind = f"vHiloActivator:= HiloActivator({hilo_periodo})|1|;"
                    hilo_strategy_sell = f"(vHiloActivator = 0)"
                    hilo_strategy_buy = f"(vHiloActivator = 1)"
                    hilo_invert = True if hilo_invert == "Sim" else False
                    if hilo_invert:
                       hilo_strategy_sell = hilo_strategy_sell.replace("0", "1")
                       hilo_strategy_buy = hilo_strategy_buy.replace("1", "0")
                    if hilo_side == "Compra":
                        if hilo_exit == "Saída":
                            exit_buy_strategies.append(hilo_strategy_buy)
                        elif hilo_exit == "Entrada":
                            buy_strategies.append(hilo_strategy_buy)
                        elif hilo_exit == "Entrada/Saída":
                            exit_buy_strategies.append(hilo_strategy_buy)
                            buy_strategies.append(hilo_strategy_buy)
                    elif hilo_side == "Venda":
                        if hilo_exit == "Saída":
                            exit_sell_strategies.append(hilo_strategy_sell)
                        elif hilo_exit == "Entrada":
                            sell_strategies.append(hilo_strategy_sell)
                        elif hilo_exit == "Entrada/Saída":
                            exit_sell_strategies.append(hilo_strategy_sell)
                            sell_strategies.append(hilo_strategy_sell)     
                    elif hilo_side == "Ambos":
                        if hilo_exit == "Saída":
                            exit_sell_strategies.append(hilo_strategy_sell)
                            exit_buy_strategies.append(hilo_strategy_buy)
                        elif hilo_exit == "Entrada":
                            buy_strategies.append(hilo_strategy_buy)
                            sell_strategies.append(hilo_strategy_sell)
                        elif hilo_exit == "Entrada/Saída":
                            exit_buy_strategies.append(hilo_strategy_buy)
                            buy_strategies.append(hilo_strategy_buy)
                            exit_sell_strategies.append(hilo_strategy_sell)
                            sell_strategies.append(hilo_strategy_sell)
                    indicatos.append(hilo_ind)
                   
 

                    if hilo_periodo is None or hilo_side is None or hilo_invert is None:
                        all_inputs_filled = False
        



                    #INDICADOR MACD

                elif option == estrategias[7]:
                    st.title(f"{option}")
                    macd_mm1  = st.number_input("", value=None, placeholder="Selecione o período da média móvel rápida para MACD", step=1, format="%d")
                    macd_mm2  = st.number_input("", value=None, placeholder="Selecione o período da média móvel lenta para MACD", step=1, format="%d")
                    macd_signal = st.number_input("", value=None, placeholder="Selecione o período do sinal para MACD", step=1, format="%d")
                    macd_side = st.selectbox("Selecione o tipo de estratégia do MACD",("Compra", "Venda","Ambos"),)
                    macd_exit = st.selectbox("Selecione o tipo de posição do MACD",("Entrada", "Saída", "Entrada/Saída"))
                    macd_invert = st.selectbox("Operar Invertido com MACD?",("Não", "Sim"),)
                    macd_var = f"vMACD: float;"
                    macdexp_var = f"vMACDEXP: float;"
                    var.append(macd_var)
                    var.append(macdexp_var)
                    macd_ind = f"vMACD:= MACD({macd_mm2},{macd_mm1},{macd_signal});"
                    indicatos.append(macd_ind)
                    macdEXP_ind = f"vMACDEXP:= MediaEXP({macd_signal},MACD({macd_mm2},{macd_mm1},{macd_signal}));"
                    macd_invert = True if macd_invert == "Sim" else False
                    if macd_invert:
                        macd_strategy_sell = f"(vMACD < vMACDEXP) "
                        macd_strategy_buy = f"(vMACD > vMACDEXP)"           
                    else:
                        macd_strategy_sell = f"(vMACD > vMACDEXP) "
                        macd_strategy_buy = f"(vMACD < vMACDEXP)"   
                    if macd_side == "Compra":
                        if macd_exit == "Saída":
                            exit_buy_strategies.append(macd_strategy_buy)
                        elif macd_exit == "Entrada":
                            buy_strategies.append(macd_strategy_buy)
                        elif macd_exit == "Entrada/Saída":
                            exit_buy_strategies.append(macd_strategy_buy)
                            buy_strategies.append(macd_strategy_buy)
                    elif macd_side == "Venda":
                        if macd_exit == "Saída":
                            exit_sell_strategies.append(macd_strategy_sell)
                        elif macd_exit == "Entrada":
                            sell_strategies.append(macd_strategy_sell)
                        elif macd_exit == "Entrada/Saída":
                            exit_sell_strategies.append(macd_strategy_sell)
                            sell_strategies.append(macd_strategy_sell)     
                    elif macd_side == "Ambos":
                        if macd_exit == "Saída":
                            exit_sell_strategies.append(macd_strategy_sell)
                            exit_buy_strategies.append(macd_strategy_buy)
                        elif macd_exit == "Entrada":
                            buy_strategies.append(macd_strategy_buy)
                            sell_strategies.append(macd_strategy_sell)
                        elif macd_exit == "Entrada/Saída":
                            exit_buy_strategies.append(macd_strategy_buy)
                            buy_strategies.append(macd_strategy_buy)
                            exit_sell_strategies.append(macd_strategy_sell)
                            sell_strategies.append(macd_strategy_sell) 
                    indicatos.append(macd_ind)
                    indicatos.append(macdEXP_ind)          


                    if macd_mm1 is None or macd_mm2 is None or macd_signal is None or macd_invert is None:
                        all_inputs_filled = False

                    #INDICADOR ESTOCASTICO
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:
                    #COMEÇOU A CÓPIA DO VETOR AQUI:

                elif option == estrategias[8]:
                    st.title(f"{option}")
                    estoc_periodo  = st.number_input("", value=None, placeholder="Selecione o período do Estocastico", step=1, format="%d")
                    estoc_periodo_media  = st.number_input("", value=None, placeholder="Selecione o período da média do Estocastico", step=1, format="%d")
                    estoc_tipo_media  = st.selectbox("Qual o tipo da média do Estocastico?",("Aritmética", "Exponencial","Welles Wilder","Ponderada"),)
                    if estoc_tipo_media == "Aritmética":
                       estoc_tipo_media = 0
                    elif estoc_tipo_media == "Exponencial":
                       estoc_tipo_media = 1
                    elif estoc_tipo_media == "Welles Wilder":
                       estoc_tipo_media = 2
                    elif estoc_tipo_media == "Ponderada":
                       estoc_tipo_media = 3
                    estoc_superior = st.number_input("", value=None, placeholder="Selecione o Estocastico superior", step=1, format="%d")
                    estoc_inferior = st.number_input("", value=None, placeholder="Selecione o Estocastico inferior", step=1, format="%d")
                    estoc_invert = st.selectbox("Operar Invertido o Estocastico?",("Não", "Sim"),)
                    estoc_side = st.selectbox("Selecione o tipo de estratégia do Estocastico",("Compra", "Venda","Ambos"),)
                    estoc_exit = st.selectbox("Selecione o tipo de posição do Estocastico",("Entrada", "Saída", "Entrada/Saída"))
                    estoc_var = f"{floats_select_dict[option]}: integer;"
                    var.append(estoc_var)
                    estoc_ind = f"vFullStochastic:= FullStochastic({estoc_periodo},{estoc_periodo_media},{estoc_tipo_media});"
                    estoc_invert = True if estoc_invert == "Sim" else False
                    if estoc_invert:
                        estoc_strategy_sell = f"(vFullStochastic < {estoc_inferior})"
                        estoc_strategy_buy = f"(vFullStochastic > {estoc_superior})" 
                    else:
                        estoc_strategy_sell = f"(vFullStochastic > {estoc_superior})" 
                        estoc_strategy_buy = f"(vFullStochastic < {estoc_inferior})"                      
                    if estoc_side == "Compra":
                        if estoc_exit == "Saída":
                            exit_buy_strategies.append(estoc_strategy_buy)
                        elif estoc_exit == "Entrada":
                            buy_strategies.append(estoc_strategy_buy)
                        elif estoc_exit == "Entrada/Saída":
                            exit_buy_strategies.append(estoc_strategy_buy)
                            buy_strategies.append(estoc_strategy_buy)
                    elif estoc_side == "Venda":
                        if estoc_exit == "Saída":
                            exit_sell_strategies.append(estoc_strategy_sell)
                        elif estoc_exit == "Entrada":
                            sell_strategies.append(estoc_strategy_sell)
                        elif estoc_exit == "Entrada/Saída":
                            exit_sell_strategies.append(estoc_strategy_sell)
                            sell_strategies.append(estoc_strategy_sell)     
                    elif estoc_side == "Ambos":
                        if estoc_exit == "Saída":
                            exit_sell_strategies.append(estoc_strategy_sell)
                            exit_buy_strategies.append(estoc_strategy_buy)
                        elif estoc_exit == "Entrada":
                            buy_strategies.append(estoc_strategy_buy)
                            sell_strategies.append(estoc_strategy_sell)
                        elif estoc_exit == "Entrada/Saída":
                            exit_buy_strategies.append(estoc_strategy_buy)
                            buy_strategies.append(estoc_strategy_buy)
                            exit_sell_strategies.append(estoc_strategy_sell)
                            sell_strategies.append(estoc_strategy_sell) 
                    indicatos.append(estoc_ind)


                    if estoc_periodo is None or estoc_periodo_media is None or estoc_tipo_media is None or estoc_superior is None or estoc_inferior is None or estoc_invert is None or estoc_side is None:
                        all_inputs_filled = False


                    #INDICADOR STOP ATR
                    #INDICADOR STOP ATR
                    #INDICADOR STOP ATR
                    #INDICADOR STOP ATR

                elif option == estrategias[9]:
                    st.title(f"{option}")
                    atr_periodo  = st.number_input("", value=None, placeholder="Selecione o período do StopATR", step=1, format="%d")
                    atr_periodo2  = st.number_input("", value=None, placeholder="Selecione o período ", step=1, format="%d")
                    atr_desv  = st.number_input("", value=None, placeholder="Selecione o desvio do StopATR", step=1, format="%d")
                    atr_tipo_media  = st.selectbox("Qual o tipo da média do StopATR?",("Aritmética", "Exponencial","Welles Wilder","Ponderada"),)
                    atr_invert = st.selectbox("Operar Invertido o StopATR?",("Não", "Sim"),)
                    atr_side = st.selectbox("Selecione o tipo de estratégia do Estocastico",("Compra", "Venda","Ambos"),)
                    atr_exit = st.selectbox("Selecione o tipo de posição do StopATR",("Entrada", "Saída", "Entrada/Saída"))
                    if atr_tipo_media == "Aritmética":
                       atr_tipo_media = 0
                    elif atr_tipo_media == "Exponencial":
                       atr_tipo_media = 1
                    elif atr_tipo_media == "Welles Wilder":
                       atr_tipo_media = 2
                    elif atr_tipo_media == "Ponderada":
                       atr_tipo_media = 3
                    atr_var = f"vStopATR: float;"
                    atr_period2_var = f"vStopATRMed: float;"
                    var.append(atr_var)
                    var.append(atr_period2_var)
                    atr_ind = f"vStopATR:= StopATR({atr_desv},{atr_periodo},{atr_tipo_media});" 
                    atr_ind_periodo2 = f"vStopATRMed:= Media({atr_periodo2},StopATR({atr_desv},{atr_periodo},{atr_tipo_media}));"
                    atr_invert = True if atr_invert == "Sim" else False
                    if atr_invert:
                        atr_strategy_sell = f"(vStopATR < vStopATRMed)"
                        atr_strategy_buy =  f"(vStopATR > vStopATRMed)"
                    else:
                        atr_strategy_sell = f"(vStopATR > vStopATRMed)" 
                        atr_strategy_buy = f"(vStopATR < vStopATRMed)"
                    if atr_side == "Compra":
                        if atr_exit == "Saída":
                            exit_buy_strategies.append(atr_strategy_buy)
                        elif atr_exit == "Entrada":
                            buy_strategies.append(atr_strategy_buy)
                        elif atr_exit == "Entrada/Saída":
                            exit_buy_strategies.append(atr_strategy_buy)
                            buy_strategies.append(atr_strategy_buy)
                    elif atr_side == "Venda":
                        if atr_exit == "Saída":
                            exit_sell_strategies.append(atr_strategy_sell)
                        elif atr_exit == "Entrada":
                            sell_strategies.append(atr_strategy_sell)
                        elif atr_exit == "Entrada/Saída":
                            exit_sell_strategies.append(atr_strategy_sell)
                            sell_strategies.append(atr_strategy_sell)     
                    elif atr_side == "Ambos":
                        if atr_exit == "Saída":
                            exit_sell_strategies.append(atr_strategy_sell)
                            exit_buy_strategies.append(atr_strategy_buy)
                        elif atr_exit == "Entrada":
                            buy_strategies.append(atr_strategy_buy)
                            sell_strategies.append(atr_strategy_sell)
                        elif atr_exit == "Entrada/Saída":
                            exit_buy_strategies.append(atr_strategy_buy)
                            buy_strategies.append(atr_strategy_buy)
                            exit_sell_strategies.append(atr_strategy_sell)
                            sell_strategies.append(atr_strategy_sell) 



                    indicatos.append(atr_ind)
                    indicatos.append(atr_ind_periodo2)


                    if atr_periodo is None or atr_periodo2 is None or atr_desv is None:
                        all_inputs_filled = False


                    #INDICADOR PARABOLIC
                    #INDICADOR PARABOLIC
                    #INDICADOR PARABOLIC
                    #INDICADOR PARABOLIC

                elif option == estrategias[10]:
                    st.title(f"{option}")
                    par_passo = st.number_input("", value=None, placeholder="Selecione o passo da Parabolic SAR")
                    par_limite = st.number_input("", value=None, placeholder="Selecione o limite da Parabolic SAR")
                    par_invert = st.selectbox("Operar Invertido o Parabolic SAR?",("Não", "Sim"),)
                    par_var = f"vParabolicSAR: float;"
                    var.append(par_var)
                    par_ind = f"vParabolicSAR:= ParabolicSAR({par_passo},{par_limite});"
                    par_side = st.selectbox("Selecione o tipo de estratégia do Estocastico",("Compra", "Venda","Ambos"),) 
                    par_exit = st.selectbox("Selecione o tipo de posição do StopATR",("Entrada", "Saída", "Entrada/Saída"))
                    par_invert = True if par_invert == "Sim" else False
                    if par_invert:
                        par_strategy_sell = f"(Close > vParabolicSAR)"
                        par_strategy_buy =  f"(Close < vParabolicSAR)"
                    else:
                        par_strategy_sell = f"(Close < vParabolicSAR)"
                        par_strategy_buy = f"(Close > vParabolicSAR)"

                    if par_side == "Compra":
                        if par_exit == "Saída":
                            exit_buy_strategies.append(par_strategy_buy)
                        elif par_exit == "Entrada":
                            buy_strategies.append(par_strategy_buy)
                        elif par_exit == "Entrada/Saída":
                            exit_buy_strategies.append(par_strategy_buy)
                            buy_strategies.append(par_strategy_buy)
                    elif par_side == "Venda":
                        if par_exit == "Saída":
                            exit_sell_strategies.append(par_strategy_sell)
                        elif par_exit == "Entrada":
                            sell_strategies.append(par_strategy_sell)
                        elif par_exit == "Entrada/Saída":
                            exit_sell_strategies.append(par_strategy_sell)
                            sell_strategies.append(par_strategy_sell)     
                    elif par_side == "Ambos":
                        if par_exit == "Saída":
                            exit_sell_strategies.append(par_strategy_sell)
                            exit_buy_strategies.append(par_strategy_buy)
                        elif par_exit == "Entrada":
                            buy_strategies.append(par_strategy_buy)
                            sell_strategies.append(par_strategy_sell)
                        elif par_exit == "Entrada/Saída":
                            exit_buy_strategies.append(par_strategy_buy)
                            buy_strategies.append(par_strategy_buy)
                            exit_sell_strategies.append(par_strategy_sell)
                            sell_strategies.append(par_strategy_sell) 
                    indicatos.append(par_ind)
                    
                    if par_passo is None or par_limite is None:
                        all_inputs_filled = False


            


            

            # Exibe o botão "Gerar" (habilitado ou desabilitado, conforme o estado)
            st.title(f"Tipo de Entrada")
            trava = st.selectbox("Quantas entradas ele realizará?",("Um por vez","Quando a condição for verdadeira"),)
            contratos = st.number_input("", value=1, placeholder="Selecione o número de contratos operados (MINIS)", step=1, format="%d")
            tipo_ordem = st.selectbox("Qual o tipo de ordem enviada?",("A Mercado","Limite"),)
            tipo_entrada = st.selectbox("Qual o tipo de entrada realizada?",("Virada de sinais","Ignorar dia anterior"),)
            limite_de_entradas = st.selectbox("Limitar as estradas?",("Não limitar","Limitar as entradas"),)
            if limite_de_entradas == "Limitar as entradas":
                limites_compra = st.number_input("", placeholder="Quantas operações de Compra?", step=1, format="%d")
                limites_venda = st.number_input("",  placeholder="Quantas operações de Venda?", step=1, format="%d")
                contador_compra = ("contador_de_compra: integer;")
                contador_venda = ("contador_de_venda: integer;")
                var.append(contador_compra)
                var.append(contador_venda)
            else:
                contador_compra = None
                contador_venda = None
            if tipo_ordem == "A Mercado":
                codigo_entrada_compra = f"BuyAtMarket({contratos});"
                codigo_entrada_venda = f"SellShortAtMarket({contratos});" 
            elif tipo_ordem == "Limite":
               tipo_limite_compra = st.selectbox("Onde enviar o limite de compra?",("Abertura","Fechamento","Minima","Maxima"),) 
               tipo_limite_venda = st.selectbox("Onde enviar o limite de venda?",("Abertura","Fechamento","Minima","Maxima"),) 
               ticks_spread_compra = st.number_input("", value=None, placeholder="Selecione o número de spread que deseja colocar na estratégia de compra", step=1, format="%d")
               ticks_spread_venda = st.number_input("", value=None, placeholder="Selecione o número de spread que deseja colocar na estratégia de venda", step=1, format="%d")
               codigo_entrada_compra = f"BuyLimit({tipo_limite_compra} + MinPriceIncrement*{ticks_spread_compra},{contratos});"
               codigo_entrada_venda = f"SellShortLimit({tipo_limite_venda} - MinPriceIncrement*{ticks_spread_venda},{contratos});"




                #ajustar as travas pois elas precisam ficar do lado DO PARAMETRO DE ENTRADA -- IF MEDIA AND CONTADOR THEN BUY


##USAR O PRIEMRIO E SEGUNDO CODE COMO EXEPLO

##USAR O PRIEMRIO E SEGUNDO CODE COMO EXEPLO

##USAR O PRIEMRIO E SEGUNDO CODE COMO EXEPLO

##USAR O PRIEMRIO E SEGUNDO CODE COMO EXEPLO





            if trava == "Um por vez":
                if len(buy_strategies) == 0:
                    if contador_venda in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n end;" + "\n" + f"if not HasPosition and not (ContadorDeCandle = 1)  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies))  + "\n" + (operationssell(sell_strategies)) +f" and (contador_de_venda < {limites_venda}) then \n " +  "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;"
                        else:                        
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" +  "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n end;" +  "\n" + f"if not HasPosition  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies)) +f"and (contador_de_venda < {limites_venda}) then \n" + "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;"
                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + f"if not HasPosition and not (ContadorDeCandle = 1) then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies)) + " then "  + codigo_entrada_venda  + "\n" + "end;"
                        else:                        
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + f"if not HasPosition then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies))  + " then " + codigo_entrada_venda  + "\n" + "end;"

                elif len(sell_strategies) == 0:
                    if contador_compra in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if not HasPosition and not (ContadorDeCandle = 1) and (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + " then " +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + (operationssell(sell_strategies)) 
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if not HasPosition  and (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + " then " +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + "\n" + "end;" + (operationssell(sell_strategies))
                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition and not (ContadorDeCandle = 1) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) +  " then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" + "end;"
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + " then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" + "end; "                       
                else:
                    if contador_compra in var or contador_venda in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + "\n" + f"if not HasPosition and not (ContadorDeCandle = 1) and (contador_de_venda < {limites_venda}) and (contador_de_compra < {limites_compra})  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + " then " +  "begin \n" + codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n "  + "\n" + "end;" + (operationssell(sell_strategies)) +  "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;" 
                        else:                        
                           code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + "\n" + f"if not HasPosition and not (ContadorDeCandle = 1)  and (contador_de_venda < {limites_venda}) and (contador_de_compra < {limites_compra})  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + " then " +  "begin \n" + codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n "  + "\n" + "end;" + (operationssell(sell_strategies)) +  "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;" 

                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition and not (ContadorDeCandle = 1)  then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + " then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies))  + " then " + codigo_entrada_venda  + "\n" + "end;"
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies))  + " then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies))  + " then " + codigo_entrada_venda  + "\n" + "end;"
            
            
            elif trava == "Quando a condição for verdadeira":
                if len(buy_strategies) == 0:
                    if contador_venda in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if not (ContadorDeCandle = 1) and (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + (operationssell(sell_strategies)) 
                        else:   
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + (operationssell(sell_strategies)) 
                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not (ContadorDeCandle = 1) then" + "\n" + "begin"+ "\n"+  (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" + "end;"
                        else:   
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" 
                elif len(sell_strategies) == 0:
                    if contador_compra in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if not (ContadorDeCandle = 1) and (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + (operationssell(sell_strategies)) 
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + f"if (contador_de_compra < {limites_compra}) then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) +  "begin \n" +  codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n end;"  + "\n" + "end;" + (operationssell(sell_strategies))
                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n"+ "if not (ContadorDeCandle = 1) then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" + "end;"
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n"+ (operationsbuy(buy_strategies)) + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" 
                else:
                    if contador_compra in var or contador_venda in var:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + "\n" + f"if not (ContadorDeCandle = 1) and (contador_de_venda < {limites_venda}) and (contador_de_compra < {limites_compra})  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) +  "begin \n" + codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n "  + "\n" + "end;" + (operationssell(sell_strategies)) +  "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;" 
                        else:                        
                           code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if ContadorDeCandle = 1 then \n begin \n if isSold then \n contador_de_venda := 1 else contador_de_venda := 0; \n if isBought then \n contador_de_compra := 1 else contador_de_compra := 0; \n end;" + "\n" + f"if (contador_de_venda < {limites_venda}) and (contador_de_compra < {limites_compra})  then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) +  "begin \n" + codigo_entrada_compra + "\ncontador_de_compra:= contador_de_compra + 1;\n "  + "\n" + "end;" + (operationssell(sell_strategies)) +  "begin \n" + codigo_entrada_venda + "\ncontador_de_venda:= contador_de_venda + 1;\n end;"  + "\n" + "end;" 
                    else:
                        if tipo_entrada == "Ignorar dia anterior":
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" +   "if not (ContadorDeCandle = 1) then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" + "end;"
                        else:
                            code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" +  (operationsbuy(buy_strategies)) + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" 
            
            if trava is None or contratos is None or tipo_ordem is None or tipo_entrada is None or limite_de_entradas is None:
                all_inputs_filled = False


            st.title(f"Tipo de Saída")
            trailling = st.selectbox("Utilizar Break Evens/Trailling Stops?",("Não","Sim"))
            trailling = True if trailling == "Sim" else False
            if trailling:
                var.append(f"ts1:boolean;\nts2:boolean;\nts3:boolean;\nts4:boolean;")
                var.append("traillingprice:float;")
                qnt_trailling = st.selectbox("Quantas proteções você deseja acionar?",(1,2,3,4))
                if qnt_trailling >= 1:
                    st.write("OS VALORES DEVEM SER PROGRESSIVOS")
                    st.write("O PRIMEIRO BREAK DEVE SER MENOR QUE O SEGUNDO E ASSIM SUCESSIVAMENTE")
                    st.write("O VALOR DE COBERTURA SEMPRE DEVE SER MENOR QUE O VALOR QUE ACIONARA O RESPECTIVO BREAK EVEN/TRAILLING STOP")
                    st.write("TODOS OS VALORES ESTÃO EM PONTOS")
                    st.write("")
                    st.write("Selecione o valor que aciona o primeiro break even")
                    ts1 = st.number_input("", value=100, placeholder="Selecione o valor que aciona o primeiro break even", step=1, format="%d")
                    st.write("Selecione o valor de cobertura do primeiro break even")
                    ts1_price = st.number_input("", value=0, placeholder="Selecione o valor de cobertura do primeiro break even", step=1, format="%d")
                    codetrail_buyside = f"\nif not ts1 and (Close > BuyPrice + {ts1}) then\nbegin\nts1:=True;\ntraillingprice:=BuyPrice + {ts1_price};\nend;"
                    codetrail_sellside = f"\nif not ts1 and (Close < SellPrice - {ts1}) then\nbegin\nts1:=True;\ntraillingprice:=SellPrice -{ts1_price};\nend;"
                if qnt_trailling >= 2: 
                    st.write("Selecione o valor que aciona o SEGUNDO break even")
                    ts2 = st.number_input("", value=200, placeholder="Selecione o valor que aciona o SEGUNDO break even", step=1, format="%d")
                    st.write("Selecione o valor de cobertura do SEGUNDO break even")
                    ts2_price = st.number_input("", value=100, placeholder="Selecione o valor de cobertura do SEGUNDO break even", step=1, format="%d")
                    codetrail_buyside =codetrail_buyside + f"\nif ts1 and not ts2 and (Close > BuyPrice + {ts2}) then\nbegin\nts2:=True;\ntraillingprice:=BuyPrice + {ts2_price};\nend;"
                    codetrail_sellside =codetrail_sellside+ f"\nif not ts1 and (Close < SellPrice - {ts2}) then\nbegin\nts2:=True;\ntraillingprice:=SellPrice -{ts2_price};\nend;" 
                if qnt_trailling >= 3:
                    st.write("Selecione o valor que aciona o TERCEIRO break even") 
                    ts3 = st.number_input("", value=300, placeholder="Selecione o valor que aciona o TERCEIRO break even", step=1, format="%d")
                    st.write("Selecione o valor de cobertura do TERCEIRO break even") 
                    ts3_price = st.number_input("", value=150, placeholder="Selecione o valor de cobertura do TERCEIRO break even", step=1, format="%d")
                    codetrail_buyside =codetrail_buyside + f"\nif ts2 and not ts3 and (Close > BuyPrice + {ts3}) then\nbegin\nts3:=True;\ntraillingprice:=BuyPrice + {ts3_price};\nend;"
                    codetrail_sellside =codetrail_sellside+ f"\nif ts2 and not ts3 and (Close < SellPrice - {ts3}) then\nbegin\nts3:=True;\ntraillingprice:=SellPrice -{ts3_price};\nend;"   
                if qnt_trailling >= 4:
                    st.write("Selecione o valor que aciona o QUARTO break even") 
                    ts4 = st.number_input("", value=400, placeholder="Selecione o valor que aciona o QUARTO break even", step=1, format="%d")
                    st.write("Selecione o valor de cobertura do QUARTO break even")
                    ts4_price = st.number_input("", value=200, placeholder="Selecione o valor de cobertura do QUARTO break even", step=1, format="%d")
                    codetrail_buyside =codetrail_buyside + f"\nif ts3 and not ts4 and (Close > BuyPrice + {ts4}) then\nbegin\nts4:=True;\ntraillingprice:=BuyPrice + {ts4_price};\nend;"
                    codetrail_sellside =codetrail_sellside+ f"\nif ts3 and not ts4 and (Close < SellPrice - {ts4}) then\nbegin\nts4:=True;\ntraillingprice:=SellPrice -{ts4_price};\nend;"     
                if trava == "Um por vez":
                    if len(buy_strategies) == 0:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition then" + "\n" + "begin"+ "\n"+ (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies)) + "then " + codigo_entrada_venda  + "\n" + "end;"
                    elif len(sell_strategies) == 0:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + "then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" + "end;"
                    else:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + "if not HasPosition then" + "\n" + "begin"+ "\n" + (operationsbuy(buy_strategies)) + "then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" + "end;"
                elif trava == "Quando a condição for verdadeira":
                    if len(buy_strategies) == 0:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" + (operationsbuy(buy_strategies)) + "\n" + (operationssell(sell_strategies))+ "then "  + codigo_entrada_venda  + "\n" 
                    elif len(sell_strategies) == 0:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n"+ (operationsbuy(buy_strategies)) + "then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + "\n" 
                    else:
                        code = " var " + "\n" + (selecvars(var)) + "\n" + ("begin") + "\n" + (selecinds(indicatos)) + "\n" +  (operationsbuy(buy_strategies)) + "then " + codigo_entrada_compra + "\n" + (operationssell(sell_strategies)) + codigo_entrada_venda  + "\n" 
                
                code = code + f"\nif not HasPosition then\nbegin\nts1:=False;\nts2:=False;\nts3:=False;\nts4:=False;\nend;"
            
            tipo_saida = st.selectbox("Qual o tipo de ordem saida?",("Fixo","Indicadores","Parcial"))
            if tipo_saida == "Fixo":
                if len(buy_strategies) > 0:
                    alvo_compra = st.number_input("", value=100, placeholder="Selecione o alvo para compra", step=1, format="%d")
                    stoploss_compra = st.number_input("", value=100, placeholder="Selecione o stop loss para compra", step=1, format="%d")
                    if trailling:
                        code = code + f"\nif isBought then \n begin \n SellToCoverLimit(BuyPrice +{alvo_compra},BuyPosition);" + codetrail_buyside + f"\nif not ts1 then\ntraillingprice:= BuyPrice - {stoploss_compra};\nSellToCoverStop(traillingprice);\nend;"
                    else:
                        code = code + f"\nif isBought then \n begin \n SellToCoverLimit(BuyPrice +{alvo_compra},BuyPosition); \n SellToCoverStop(BuyPrice - {stoploss_compra},BuyPrice -{stoploss_compra},BuyPosition); \n end;"
                if len(sell_strategies) > 0:
                    alvo_venda = st.number_input("", value=100, placeholder="Selecione o alvo para venda", step=1, format="%d")
                    stoploss_venda = st.number_input("", value=100, placeholder="Selecione o stop loss para venda", step=1, format="%d")
                    if trailling:
                        code = code + f"\nif isSold then \n begin \n BuyToCoverLimit(SellPrice -{alvo_venda},SellPosition);" + codetrail_sellside + f"\nif not ts1 then\ntraillingprice:= SellPrice + {stoploss_compra};\nBuyToCoverStop(traillingprice);\nend;"
                    else:
                        code = code + f"\nif isSold then \n begin \n BuyToCoverLimit(SellPrice - {alvo_venda},SellPosition); \n BuyToCoverStop(SellPrice + {stoploss_venda},SellPrice + {stoploss_venda},SellPosition); \n end;"
            elif tipo_saida == "Indicadores":
                if len(exit_buy_strategies) > 0:
                    code = code + f"\nif isSold then \n begin \n {(operationsbuy(exit_buy_strategies))} \n BuyToCoverAtMarket(SellPosition); \n end;"
                if len(exit_sell_strategies) > 0:
                    code = code + f"\nif isBought then \n begin \n {(operationssell(exit_sell_strategies))} \n SellToCoverAtMarket(BuyPosition); \n end;" 
                if len(exit_sell_strategies) == 0 and len(exit_buy_strategies) == 0 :
                    st.title(f"Você precisa colocar algum indicador para saída!")
               
            elif tipo_saida == "Parcial":
                qnt_parcial = st.number_input("",value=1,min_value=1,max_value=contratos,placeholder=f"Quantas parciais devem sair? Você só pode ter no máximo {contratos}",step=1,format="%d")
                for i in range(qnt_parcial):
                    lvl_parc = st.number_input("",value=1,min_value=1,placeholder=f"Quais a saída da parcial {i}",step=1,format="%d")
                    if len(buy_strategies) > 0:
                        vpac = vpac + f"SellToCoverLimit(BuyPrice + {lvl_parc}); \n"
                    elif len(sell_strategies) > 0:
                        vpac = vpac + f"BuyToCoverLimit(SellPrice - {lvl_parc}); \n"
                if len(buy_strategies) > 0:
                    code = code + f"\nif isBought then \n begin \n {vpac} \n end;" 
                elif len(sell_strategies) > 0:
                    code = code + f"\nif isSold then \n begin \n {vpac} \n end;" 
                else:
                    code = code + f"\nif isBought then \n begin \n {vpac} \n end; \nif isSold then \n begin \n {vpac} \n end;" 
            if tipo_saida is None:
                all_inputs_filled = False

            if all_inputs_filled:
                st.session_state.gerar_button_enabled = True

            gerar_button = st.button("Gerar", disabled=not st.session_state.gerar_button_enabled)

            # Ação ao clicar em "Gerar"
            if gerar_button:
                st.session_state.gerar_clicked = True
                

# Exibe o texto "Oi" quando o botão "Gerar" for clicado
if st.session_state.gerar_clicked:
    code = code + "\n" + "end;"
    st.code(code)
    
    

if not st.session_state.create_clicked and not st.session_state.install_clicked:
    st.title("Acesse as barras laterais para mais informações")
    st.write("alpha version 1.0")
