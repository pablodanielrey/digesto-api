import pytest

def test_subir_archivo():
    import base64
    from sqlalchemy.orm import defer
    from digesto.model import obtener_session
    from digesto.model.Utils import md5sum
    from digesto.model.DigestoModelLocal import DigestoModelLocal
    from digesto.model.entities.Digesto import Archivo

    with obtener_session() as session:
        a = session.query(Archivo).filter(Archivo.nombre == 'prueba.pdf').options(defer('contenido')).one_or_none()
        if a:
            session.delete(a)
            session.commit()

    longitud_binaria_original = 0
    longitud_b64_original = 0
    b64_contenido_original = ''
    md5_original = ''
    aid = ''
    with open('test/prueba.pdf','rb') as f:
        contenido = f.read()
        
        ''' guardo variables de control '''
        longitud_binaria_original = len(contenido)
        b64_contenido_original = base64.b64encode(contenido).decode('utf8')
        longitud_b64_original = len(b64_contenido_original)
        md5_original = md5sum(contenido)

        with obtener_session() as session:
            aid = DigestoModelLocal.subir_archivo(session, 'prueba.pdf', contenido, 'application/pdf')
            session.commit()

            assert session.query(Archivo).filter(Archivo.id == aid).options(defer('contenido')).one_or_none() is not None

    with obtener_session() as session:
        archivo = DigestoModelLocal.obtener_archivo(session, aid)
        assert archivo is not None

        assert md5_original == archivo.hash_

        """ decodifico el contenido y lo guardo en un archivo """
        nombre = f"/tmp/{archivo.nombre}"
        with open(nombre,'wb') as f:
            b64cont = archivo.contenido
            assert b64_contenido_original == b64cont
            assert len(b64cont) == longitud_b64_original
            
            contenido = base64.b64decode(archivo.contenido.encode())
            assert len(contenido) == longitud_binaria_original

            f.write(contenido)

        """ chequeo que el hash del archivo guardado sea igual que el de la base """
        with open(nombre, 'rb') as f:
            md5s = md5sum(f.read())
            assert md5s == archivo.hash_

        """ chequeo que el hash original sea igual al calculado del archivo escrito """
        assert md5_original == md5s

    """ limpio la base nuevamente """
    with obtener_session() as session:
        a = session.query(Archivo).filter(Archivo.nombre == 'prueba.pdf').options(defer('contenido')).one_or_none()
        if a:
            session.delete(a)
            session.commit()

