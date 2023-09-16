from selene import browser, by, be, have, query
from selene.support.conditions import not_
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from functools import partial
from selenium.common.exceptions import ElementClickInterceptedException
from selene import command
import time


def get_element_active(element, next_index):
    return int(element.get(query.text)) == next_index


def pegar_espelho_grupo(elemento):
    return 'idBtnVisualizarEspelhoGrupo' in elemento.get(query.attribute('id'))


browser.open('http://dgp.cnpq.br/dgp/faces/consulta/consulta_parametrizada.jsf')

# Clique no elemento com o ID correto (usando aspas duplas no seletor CSS)
browser.element(by.name("idFormConsultaParametrizada:buscaRefinada")).should(be.visible).click()
browser.element(by.css('.control-label')).should(be.visible)
reg = browser.element(by.xpath('//div[@id="idFormConsultaParametrizada:idRegiao"]'))
reg.click()
browser.element(by.xpath('//*[@id="idFormConsultaParametrizada:idRegiao_panel"]/div/ul/li[5]')).click()
time.sleep(2)
browser.element(by.xpath('//div[@id="idFormConsultaParametrizada:idUF"]')).click()
browser.element(by.xpath('//*[@id="idFormConsultaParametrizada:idUF_panel"]/div/ul/li[3]')).click()
time.sleep(2)
browser.element(by.xpath('//div[@id="idFormConsultaParametrizada:idInst"]')).click()
browser.element(by.xpath('//*[@id="idFormConsultaParametrizada:idInst_panel"]/div/ul/li[77]')).click()
browser.element(by.xpath('//*[@id="idFormConsultaParametrizada:idPesquisar"]')).click()

time.sleep(4)
browser.element(by.xpath('//*[@id="idFormConsultaParametrizada:resultadoDataList:0:idBtnVisualizarEspelhoGrupo"]')).should(be.visible)

for index_page in range(1, 18, 1):
    active_element = int(browser.element(by.css('.ui-state-active')).get(query.text))
    pages = browser.all(by.css('.ui-paginator-page'))
    fun_next_active = partial(get_element_active, next_index=active_element+1)
    map_pages = list(filter(fun_next_active, pages))
    links = browser.all('.controls a')
    map_grupo_espelho = list(filter(pegar_espelho_grupo, links))

    for button in map_grupo_espelho[5:]:
        button.click()

        time.sleep(4)
        browser.switch_to_next_tab()
        print(browser.driver.current_url)
        browser.element(by.css('.selo-grupo')).should(be.visible)

        h1 = browser.element(by.css('h1')).get(query.text)
        h1_text = browser.element(by.xpath('//*[@id="idFormVisualizarGrupoPesquisa"]/div/div[2]')).get(query.text)
        h1_text_split = h1_text.split('espelhogrupo/')[1]
        browser.save_page_source(f'{h1_text_split}.html')
        browser.close_current_tab()
        browser.switch_to_tab(0)
        print(f'index_button: {button.get(query.text)}, index_page: {index_page}, url: {browser.driver.current_url}')
        time.sleep(4)


    map_pages[0].click()
    time.sleep(4)
    print(f'active_element: {active_element}')
    active_element = int(browser.element(by.css('.ui-state-active')).get(query.text))
    time.sleep(3)

input()

