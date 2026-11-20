package br.com.fiap.meubairro.bo;

import br.com.fiap.meubairro.dao.BairroDao;
import br.com.fiap.meubairro.dao.UsuarioDao;
import br.com.fiap.meubairro.exception.ConflitoException;
import br.com.fiap.meubairro.exception.RecursoNaoEncontradoException;
import br.com.fiap.meubairro.exception.RegraNegocioException;
import br.com.fiap.meubairro.model.Usuario;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UsuarioBO {

    private final UsuarioDao dao;
    private final BairroDao bairroDao;

    public UsuarioBO(UsuarioDao dao, BairroDao bairroDao) {
        this.dao = dao;
        this.bairroDao = bairroDao;
    }

    public Usuario criar(Usuario u) {
        validar(u, null);
        return dao.inserir(u);
    }

    public List<Usuario> listar() {
        return dao.listar();
    }

    public Usuario buscar(Long id) {
        return dao.buscarPorId(id).orElseThrow(() -> new RecursoNaoEncontradoException("Usuário", id));
    }

    public Usuario atualizar(Long id, Usuario u) {
        buscar(id);
        validar(u, id);
        dao.atualizar(id, u);
        return buscar(id);
    }

    public void remover(Long id) {
        buscar(id);
        if (dao.temDependentes(id)) {
            throw new RegraNegocioException("Usuário possui reportes ou votos e não pode ser removido");
        }
        dao.remover(id);
    }

    private void validar(Usuario u, Long ignorarId) {
        if (dao.existeEmail(u.email(), ignorarId)) {
            throw new ConflitoException("E-mail já cadastrado: " + u.email());
        }
        if (u.bairroId() != null && bairroDao.buscarPorId(u.bairroId()).isEmpty()) {
            throw new RecursoNaoEncontradoException("Bairro", u.bairroId());
        }
    }
}
