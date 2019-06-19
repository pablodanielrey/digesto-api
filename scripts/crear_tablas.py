
if __name__ == '__main__':
    from digesto.model.entities import crear_tablas
    crear_tablas()

    from digesto.model import obtener_session
    from digesto.model.entities.Digesto import TipoRelacionNorma, Emisor, TipoNorma
    import uuid

    with obtener_session() as session:

        tipos = [ 
            {
                'id':'',
                'tipo':'Deja sin efecto'
            },
            {
                'id':'',
                'tipo':'Amplía'
            },
            {
                'id':'',
                'tipo':'Modifica o Rectifica'
            }
        ]

        for t in tipos:
            if session.query(TipoRelacionNorma).filter(TipoRelacionNorma.tipo == t).count() <= 0:
                tn = TipoRelacionNorma()
                tn.id = t['id']
                tn.tipo = t['tipo']
                session.add(tn)
                session.commit()

        tipos = ['Disposición','Ordenanza','Resolución']
        for t in tipos:
            if session.query(TipoNorma).filter(TipoNorma.tipo == t).count() <= 0:
                tn = TipoNorma()
                tn.id = str(uuid.uuid4())
                tn.tipo = t
                session.add(tn)
                session.commit()

        emisores = ['Consejo Directivo', 'Secretaría Académica', 'Secretaría de Extensión', 'Decano', 'Vicedecano']
        for e in emisores:
            if session.query(Emisor).filter(Emisor.nombre == e).count() <= 0:
                tn = Emisor()
                tn.id = str(uuid.uuid4())
                tn.nombre = e
                session.add(tn)
                session.commit()        