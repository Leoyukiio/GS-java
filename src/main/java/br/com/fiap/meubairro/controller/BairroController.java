package br.com.fiap.meubairro.controller;

import br.com.fiap.meubairro.bo.BairroBO;
import br.com.fiap.meubairro.model.Bairro;
import br.com.fiap.meubairro.model.BairroResumo;
import br.com.fiap.meubairro.model.IndicadorBairro;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping
public class BairroController {

    private final BairroBO bo;

    public BairroController(BairroBO bo) {
        this.bo = bo;
    }

    @PostMapping("/bairros")
    public ResponseEntity<Bairro> criar(@Valid @RequestBody Bairro bairro) {
        Bairro criado = bo.criar(bairro);
        URI uri = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(criado.id()).toUri();
        return ResponseEntity.created(uri).body(criado);
    }

    @GetMapping("/bairros")
    public List<Bairro> listar() {
        return bo.listar();
    }

    @GetMapping("/bairros/{id}")
    public BairroResumo detalhar(@PathVariable Long id) {
        return bo.detalhar(id);
    }

    @PutMapping("/bairros/{id}")
    public Bairro atualizar(@PathVariable Long id, @Valid @RequestBody Bairro bairro) {
        return bo.atualizar(id, bairro);
    }

    @DeleteMapping("/bairros/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void remover(@PathVariable Long id) {
        bo.remover(id);
    }

    @GetMapping("/bairros/{id}/indicadores")
    public IndicadorBairro indicadores(@PathVariable Long id) {
        return bo.buscarIndicadores(id);
    }

    @PutMapping("/bairros/{id}/indicadores")
    public IndicadorBairro salvarIndicadores(@PathVariable Long id, @Valid @RequestBody IndicadorBairro indicadores) {
        return bo.salvarIndicadores(id, indicadores);
    }

    @GetMapping("/ranking")
    public List<BairroResumo> ranking() {
        return bo.ranking();
    }
}
