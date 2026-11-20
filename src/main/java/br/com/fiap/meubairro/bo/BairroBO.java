package br.com.fiap.meubairro.bo;

import br.com.fiap.meubairro.dao.BairroDao;
import br.com.fiap.meubairro.dao.IndicadorBairroDao;
import br.com.fiap.meubairro.exception.ConflitoException;
import br.com.fiap.meubairro.exception.RecursoNaoEncontradoException;
import br.com.fiap.meubairro.exception.RegraNegocioException;
import br.com.fiap.meubairro.model.Bairro;
import br.com.fiap.meubairro.model.BairroResumo;
import br.com.fiap.meubairro.model.IndicadorBairro;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class BairroBO {

    private static final BigDecimal P_INFRA = new BigDecimal("0.35");
    private static final BigDecimal P_SEG = new BigDecimal("0.25");
    private static final BigDecimal P_SERV = new BigDecimal("0.20");
    private static final BigDecimal P_LAZER = new BigDecimal("0.20");

    private final BairroDao dao;
    private final IndicadorBairroDao indicadorDao;

    public BairroBO(BairroDao dao, IndicadorBairroDao indicadorDao) {
        this.dao = dao;
        this.indicadorDao = indicadorDao;
    }

    public Bairro criar(Bairro b) {
        validarDuplicidade(b, null);
        return dao.inserir(b);
    }

    public List<Bairro> listar() {
        return dao.listar();
    }

    public Bairro buscar(Long id) {
        return dao.buscarPorId(id).orElseThrow(() -> new RecursoNaoEncontradoException("Bairro", id));
    }

    public Bairro atualizar(Long id, Bairro b) {
        buscar(id);
        validarDuplicidade(b, id);
        dao.atualizar(id, b);
        return buscar(id);
    }

    @Transactional
    public void remover(Long id) {
        buscar(id);
        if (dao.temDependentes(id)) {
            throw new RegraNegocioException("Bairro possui reportes ou usuários vinculados e não pode ser removido");
        }
        indicadorDao.removerPorBairro(id);
        dao.remover(id);
    }

    public IndicadorBairro buscarIndicadores(Long bairroId) {
        buscar(bairroId);
        return indicadorDao.buscarPorBairro(bairroId)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Indicadores do bairro", bairroId));
    }

    public IndicadorBairro salvarIndicadores(Long bairroId, IndicadorBairro in) {
        buscar(bairroId);
        indicadorDao.salvar(bairroId, in);
        return buscarIndicadores(bairroId);
    }

    public BairroResumo detalhar(Long id) {
        Bairro b = buscar(id);
        IndicadorBairro ind = indicadorDao.buscarPorBairro(id).orElse(null);
        List<BairroResumo> ranking = ranking();
        return ranking.stream().filter(r -> r.bairro().id().equals(id)).findFirst()
                .orElse(new BairroResumo(b, ind, calcularNota(ind), null));
    }

    public List<BairroResumo> ranking() {
        Map<Long, IndicadorBairro> indicadores = indicadorDao.listar().stream()
                .collect(Collectors.toMap(IndicadorBairro::bairroId, Function.identity()));

        List<BairroResumo> comNota = new ArrayList<>();
        List<BairroResumo> semNota = new ArrayList<>();
        for (Bairro b : dao.listar()) {
            IndicadorBairro ind = indicadores.get(b.id());
            if (ind == null) semNota.add(new BairroResumo(b, null, null, null));
            else comNota.add(new BairroResumo(b, ind, calcularNota(ind), null));
        }
        comNota.sort(Comparator.comparing(BairroResumo::nota).reversed());

        List<BairroResumo> resultado = new ArrayList<>();
        for (int i = 0; i < comNota.size(); i++) {
            BairroResumo r = comNota.get(i);
            resultado.add(new BairroResumo(r.bairro(), r.indicadores(), r.nota(), i + 1));
        }
        resultado.addAll(semNota);
        return resultado;
    }

    public BigDecimal calcularNota(IndicadorBairro i) {
        if (i == null) return null;
        return i.infraestrutura().multiply(P_INFRA)
                .add(i.seguranca().multiply(P_SEG))
                .add(i.servicos().multiply(P_SERV))
                .add(i.lazer().multiply(P_LAZER))
                .setScale(1, RoundingMode.HALF_UP);
    }

    private void validarDuplicidade(Bairro b, Long ignorarId) {
        if (dao.existeNomeNaCidade(b.nome(), b.cidade(), ignorarId)) {
            throw new ConflitoException("Já existe o bairro '" + b.nome() + "' em " + b.cidade());
        }
    }
}
