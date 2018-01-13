# NMR Demo

**Requires an installation of isaDream**.

## Simple Deployment

This can be deployed in a standalone fashion for testing by running the bokeh serve command from within parent directory of NMRDemo.

```
bokeh serve NMRDemo/
```

## TODO

- [x] Add a title div.
- [x] Add a plot / figure title that updates according to the selections.
- [x] Format the metadata selection paragraph so it is readable / useful.
	- [x] Explore conversion into an ISA object.
	- [x] Move to the right hand side of the plot.
- [x] Filter the options available in the X and Y drop down selectors.
- [x] Add a color by drop down.
- [x] Add counter-ion functionality.
	- [x] Create the FactorValue instances for each Sample() instance.
	- [x] Create the counter_ion StudyFactor.
- [x] Add a size drop down.
- [x] Change theme or colors for visibility.
- [x] Add a legend to the plot / figure.
- [ ] Add more metadata information in the metadata div element.
	- [x] NMR acquisition information.
		- [x] Create OntologyAnnotations.
		- [x] Create ProtocolParameters.
		- [x] Create associated OntologyAnnotations.
		- [x] Pass the process information to the metadata display div.
		- [x] Create Process for each assay.
- [ ] Add more data points.
	- [x] Sipos 2006 Tantala figure 2.
	- [ ] Moolenar 1970
- [ ] Add counter ion concentration feature.
- [ ] Sample progeny information display.
- [ ] Create user-friendly strings for column names.
- [ ] Add a log scale toggle.
- [ ] Add a unique marker drop down.

## TODO: Demo Presentation

- [x] Prepare / update poster. 10:00 AM tomorrow morning.
- [ ] Prepare ISA document diagram.

## TODO: Yak-shaving

- [ ] Update Bokeh layout elements by name, rather than nested indexes.
- [ ] Change the demo data generation to a function.
- [ ] Find a more elegant way to format python lists to html output.