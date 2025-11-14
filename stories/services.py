"""
Serviço para geração de histórias com IA
TODO: Integrar com OpenAI API no futuro
"""


def generate_story(pet, moments):
    """
    Gera uma história fictícia baseada no pet e seus momentos.
    
    TODO: Substituir por chamada real à OpenAI API:
    
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    prompt = f"Crie uma história encantadora sobre {pet.name}, um {pet.species}..."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    """
    
    # Simulação de geração de IA
    texto = f"# A História de {pet.name}\n\n"
    
    if pet.species == 'dog':
        especie_texto = "cachorro"
    elif pet.species == 'cat':
        especie_texto = "gato"
    elif pet.species == 'bird':
        especie_texto = "pássaro"
    elif pet.species == 'rabbit':
        especie_texto = "coelho"
    else:
        especie_texto = "pet"
    
    texto += f"Esta é a história encantadora de {pet.name}, um {especie_texto} especial que trouxe muita alegria e amor para a vida de seus tutores.\n\n"
    
    if pet.birth_date:
        texto += f"Desde o dia {pet.birth_date.strftime('%d/%m/%Y')}, {pet.name} começou a fazer parte desta família.\n\n"
    
    texto += "## Momentos Especiais\n\n"
    
    for i, momento in enumerate(moments, 1):
        texto += f"### {momento.title}\n\n"
        texto += f"{momento.text}\n\n"
    
    texto += f"\n\n{pet.name} é mais do que um {especie_texto}, é um membro da família que trouxe momentos inesquecíveis e muito carinho. Cada dia ao lado de {pet.name} é uma nova aventura e uma nova razão para sorrir.\n\n"
    texto += "---\n\n"
    texto += "*História gerada com IA - PetStory*"
    
    return texto

