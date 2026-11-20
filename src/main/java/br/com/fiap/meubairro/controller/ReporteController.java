package br.com.fiap.meubairro.controller;

import br.com.fiap.meubairro.bo.ReporteBO;
import br.com.fiap.meubairro.bo.VotoBO;
import br.com.fiap.meubairro.model.Categoria;
import br.com.fiap.meubairro.model.Reporte;
import br.com.fiap.meubairro.model.Status;
import br.com.fiap.meubairro.model.Voto;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/reportes")
public class ReporteController {

    public record AlteracaoStatus(@NotNull(message = "status é obrigatório") Status status,
                                  @NotNull(message = "adminId é obrigatório") Long adminId) {
    }

    private final ReporteBO bo;
    private final VotoBO votoBO;

    public ReporteController(ReporteBO bo, VotoBO votoBO) {
        this.bo = bo;
        this.votoBO = votoBO;
    }

    @PostMapping
    public ResponseEntity<Reporte> criar(@Valid @RequestBody Reporte reporte) {
        Reporte criado = bo.criar(reporte);
        URI uri = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(criado.id()).toUri();
        return ResponseEntity.created(uri).body(criado);
    }

    @GetMapping
    public List<Reporte> listar(@RequestParam(required = false) Long bairroId,
                                @RequestParam(required = false) Status status,
                                @RequestParam(required = false) Categoria categoria) {
        return bo.listar(bairroId, status, categoria);
    }

    @GetMapping("/{id}")
    public Reporte buscar(@PathVariable Long id) {
        return bo.buscar(id);
    }

    @PutMapping("/{id}")
    public Reporte atualizar(@PathVariable Long id, @Valid @RequestBody Reporte reporte) {
        return bo.atualizar(id, reporte);
    }

    @PutMapping("/{id}/status")
    public Reporte alterarStatus(@PathVariable Long id, @Valid @RequestBody AlteracaoStatus corpo) {
        return bo.alterarStatus(id, corpo.status(), corpo.adminId());
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void remover(@PathVariable Long id) {
        bo.remover(id);
    }

    @PostMapping("/{id}/votos")
    public ResponseEntity<Voto> votar(@PathVariable Long id, @Valid @RequestBody Voto voto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(votoBO.votar(id, voto.usuarioId()));
    }

    @GetMapping("/{id}/votos")
    public List<Voto> votos(@PathVariable Long id) {
        return votoBO.listar(id);
    }

    @DeleteMapping("/{id}/votos/{usuarioId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void removerVoto(@PathVariable Long id, @PathVariable Long usuarioId) {
        votoBO.removerVoto(id, usuarioId);
    }
}
