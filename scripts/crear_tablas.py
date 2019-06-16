
if __name__ == '__main__':
    from digesto.model.entities import crear_tablas
    crear_tablas()

    from digesto.model import obtener_session
    from digesto.model.entities.Digesto import TipoRelacionNorma
    import uuid

    with obtener_session() as session:

        tipos = ['Deja sin efecto','Amplía','Modifica o Rectifica']
        for t in tipos:
            if session.query(TipoRelacionNorma).filter(TipoRelacionNorma.tipo == t).count() <= 0:
                tn = TipoRelacionNorma()
                tn.id = str(uuid.uuid4())
                tn.tipo = t
                session.add(tn)
                session.commit()