package br.com.fiap.meubairro.bo;

import br.com.fiap.meubairro.dao.BairroDao;
import br.com.fiap.meubairro.dao.ReporteDao;
import br.com.fiap.meubairro.dao.UsuarioDao;
import br.com.fiap.meubairro.dao.VotoDao;
import br.com.fiap.meubairro.exception.RecursoNaoEncontradoException;
import br.com.fiap.meubairro.exception.RegraNegocioException;
import br.com.fiap.meubairro.model.Categoria;
import br.com.fiap.meubairro.model.Perfil;
import br.com.fiap.meubairro.model.Reporte;
import br.com.fiap.meubairro.model.Status;
import br.com.fiap.meubairro.model.Usuario;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ReporteBO {

    private final ReporteDao dao;
    private final VotoDao votoDao;
    private final BairroDao bairroDao;
    private final UsuarioDao usuarioDao;

    public ReporteBO(ReporteDao dao, VotoDao votoDao, BairroDao bairroDao, UsuarioDao usuarioDao) {
        this.dao = dao;
        this.votoDao = votoDao;
        this.bairroDao = bairroDao;
        this.usuarioDao = usuarioDao;
    }

    public Reporte criar(Reporte r) {
        usuarioDao.buscarPorId(r.usuarioId())
                .orElseThrow(() -> new RecursoNaoEncontradoException("Usuário", r.usuarioId()));
        validarBairro(r.bairroId());
        return dao.inserir(r);
    }

    public List<Reporte> listar(Long bairroId, Status status, Categoria categoria) {
        return dao.listar(bairroId, status, categoria);
    }

    public Reporte buscar(Long id) {
        return dao.buscarPorId(id).orElseThrow(() -> new RecursoNaoEncontradoException("Reporte", id));
    }

    public Reporte atualizar(Long id, Reporte r) {
        Reporte atual = buscar(id);
        if (atual.status() == Status.RESOLVIDO) {
            throw new RegraNegocioException("Reporte já resolvido não pode ser editado");
        }
        validarBairro(r.bairroId());
        dao.atualizarDados(id, r);
        return buscar(id);
    }

    public Reporte alterarStatus(Long id, Status novo, Long adminId) {
        Reporte atual = buscar(id);
        Usuario admin = usuarioDao.buscarPorId(adminId)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Usuário", adminId));
        if (admin.perfil() != Perfil.ADMIN) {
            throw new RegraNegocioException("Apenas usuários ADMIN podem alterar o status de um reporte");
        }
        if (novo.ordinal() <= atual.status().ordinal()) {
            throw new RegraNegocioException(
                    "Transição inválida: " + atual.status() + " -> " + novo + " (o status só pode avançar)");
        }
        dao.atualizarStatus(id, novo);
        return buscar(id);
    }

    @Transactional
    public void remover(Long id) {
        buscar(id);
        votoDao.removerPorReporte(id);
        dao.remover(id);
    }

    private void validarBairro(Long bairroId) {
        bairroDao.buscarPorId(bairroId).orElseThrow(() -> new RecursoNaoEncontradoException("Bairro", bairroId));
    }
}
