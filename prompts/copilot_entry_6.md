Its very unclear what the calc is supposed to be here:   def test_cosine_values():
        assert cosine([1.0, 0.0], [2.0, 0.0]) == pytest.approx(1.0)
>       assert cosine([1.0, 0.0], [0.0, 3.0]) == pytest.approx(0.0)
E       assert 1.0 == 0.0 ± 1.0e-12
