
if __name__ == '__main__':
    from digesto.model.entities import crear_tablas
    crear_tablas()

    from digesto.model import obtener_session
    from digesto.model.entities.Digesto import TipoRelacionNorma, Emisor, TipoNorma
    from digesto.model.entities.Google import Sincronizacion
    import uuid

    with obtener_session() as session:

        tipos = [ 
            {
                'id':'e60fbaa0-cebb-4c45-bfc6-c35ac1265bd6',
                'tipo':'Deja sin efecto'
            },
            {
                'id':'546057a1-79ff-4002-a321-0d1c60c287bd',
                'tipo':'Amplía'
            },
            {
                'id':'8985566a-901a-473c-ab5d-a5081d27b738',
                'tipo':'Modifica o Rectifica'
            }
        ]

        for t in tipos:
            if session.query(TipoRelacionNorma).filter(TipoRelacionNorma.id == t['id']).count() <= 0:
                tn = TipoRelacionNorma()
                tn.id = t['id']
                tn.tipo = t['tipo']
                session.add(tn)
                session.commit()

        tipos = [ 
            {
                'id':'2956717d-81b2-43b4-8360-b212f58282f0',
                'tipo':'Disposición'
            },
            {
                'id':'d50b83a3-6408-4883-bff0-83d32c0935f8',
                'tipo':'Ordenanza'
            },
            {
                'id':'ef62801a-3c10-436e-8265-4f601cf93748',
                'tipo':'Resolución'
            }
        ]

        for t in tipos:
            if session.query(TipoNorma).filter(TipoNorma.id == t['id']).count() <= 0:
                tn = TipoNorma()
                tn.id = str(uuid.uuid4())
                tn.tipo = t
                session.add(tn)
                session.commit()

        emisores = ['Consejo Directivo', 'Secretaría Académica', 'Secretaría de Extensión', 'Decano', 'Vicedecano']
        emisores = [ 
            {
                'id':'608b2f58-239e-4f31-80ab-5739adebb5d5',
                'tipo':'Consejo Directivo'
            },
            {
                'id':'d3a4e464-305f-41ad-ae7c-4630a843b91a',
                'tipo':'Secretaría Académica'
            },
            {
                'id':'a73ed002-1b33-442d-b539-e8dcfff51a9a',
                'tipo':'Secretaría de Extensión'
            },
            {
                'id':'c7a62f00-4260-4f44-941e-157ac7125fc5',
                'tipo':'Decano'
            },
            {
                'id':'2e6a6d02-24ee-49a7-873b-92219ea07345',
                'tipo':'Vicedecano'
            }
        ]        
        for e in emisores:
            if session.query(Emisor).filter(Emisor.id == e['id']).count() <= 0:
                tn = Emisor()
                tn.id = str(uuid.uuid4())
                tn.nombre = e
                session.add(tn)
                session.commit()        