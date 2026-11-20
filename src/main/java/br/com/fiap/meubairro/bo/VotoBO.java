package br.com.fiap.meubairro.bo;

import br.com.fiap.meubairro.dao.ReporteDao;
import br.com.fiap.meubairro.dao.UsuarioDao;
import br.com.fiap.meubairro.dao.VotoDao;
import br.com.fiap.meubairro.exception.ConflitoException;
import br.com.fiap.meubairro.exception.RecursoNaoEncontradoException;
import br.com.fiap.meubairro.exception.RegraNegocioException;
import br.com.fiap.meubairro.model.Reporte;
import br.com.fiap.meubairro.model.Status;
import br.com.fiap.meubairro.model.Voto;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class VotoBO {

    private final VotoDao dao;
    private final ReporteDao reporteDao;
    private final UsuarioDao usuarioDao;

    public VotoBO(VotoDao dao, ReporteDao reporteDao, UsuarioDao usuarioDao) {
        this.dao = dao;
        this.reporteDao = reporteDao;
        this.usuarioDao = usuarioDao;
    }

    public Voto votar(Long reporteId, Long usuarioId) {
        Reporte r = buscarReporte(reporteId);
        usuarioDao.buscarPorId(usuarioId).orElseThrow(() -> new RecursoNaoEncontradoException("Usuário", usuarioId));
        if (r.usuarioId().equals(usuarioId)) {
            throw new RegraNegocioException("O autor não pode votar no próprio reporte");
        }
        if (r.status() == Status.RESOLVIDO) {
            throw new RegraNegocioException("Reporte resolvido não aceita novos votos");
        }
        if (dao.existe(reporteId, usuarioId)) {
            throw new ConflitoException("Usuário já confirmou este reporte");
        }
        return dao.inserir(reporteId, usuarioId);
    }

    public List<Voto> listar(Long reporteId) {
        buscarReporte(reporteId);
        return dao.listarPorReporte(reporteId);
    }

    public void removerVoto(Long reporteId, Long usuarioId) {
        buscarReporte(reporteId);
        if (dao.remover(reporteId, usuarioId) == 0) {
            throw new RecursoNaoEncontradoException("Voto do usuário " + usuarioId + " no reporte", reporteId);
        }
    }

    private Reporte buscarReporte(Long id) {
        return reporteDao.buscarPorId(id).orElseThrow(() -> new RecursoNaoEncontradoException("Reporte", id));
    }
}
