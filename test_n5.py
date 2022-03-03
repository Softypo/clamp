from dataclasses import dataclass, field
import h5py as h5
from ast import literal_eval


@dataclass
class dvh5():
    file_path: str
    full_load: bool = True

    def __post_init__(self):
        self.data = self.__dvh5_reader()
        self.well = self.data['attrs']['name']

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()

    def __dvh5_reader(self):
        def h5dump(f, h5dict={}):
            for key in f.keys():
                if isinstance(f[key], h5._hl.group.Group):
                    if f[key].attrs:
                        if f.name == '/':
                            h5dict.update(
                                {'attrs': attrs_parser(f[key].attrs)})
                        else:
                            h5dict[f.name] = {
                                'attrs': attrs_parser(f[key].attrs)}
                    h5dump(f[key])
                elif isinstance(f[key], h5._hl.dataset.Dataset):
                    if self.full_load:
                        h5dict['/'.join(f[key].parent.name.split('/')[2:])] = h5dict.setdefault('/'.join(f[key].parent.name.split('/')[2:]), {}) | {
                            key: {'array': f[key][:], 'attrs': attrs_parser(f[key].attrs) if f[key].attrs else None}}
                    else:
                        h5dict['/'.join(f[key].parent.name.split('/')[2:])] = h5dict.setdefault('/'.join(f[key].parent.name.split('/')[2:]), {}) | {key: {
                            'shape': f[key].shape, 'attrs': attrs_parser(f[key].attrs) if f[key].attrs else None}}
            return h5dict

        def attrs_parser(attrs):
            return {k: literal_eval(v) if isinstance(v, str) and '{' in v else v for k, v in attrs.items()}

        with h5.File(self.file_path, 'r') as f:
            return h5dump(f)


def dvh5_reader(file_path, full_load=True):
    def h5dump(f, h5dict={}):
        for key in f.keys():
            if isinstance(f[key], h5._hl.group.Group):
                if f[key].attrs:
                    if f.name == '/':
                        h5dict.update({'attrs': attrs_parser(f[key].attrs)})
                    else:
                        h5dict[f.name] = {'attrs': attrs_parser(f[key].attrs)}
                h5dump(f[key])
            elif isinstance(f[key], h5._hl.dataset.Dataset):
                if full_load:
                    h5dict['/'.join(f[key].parent.name.split('/')[2:])] = h5dict.setdefault('/'.join(f[key].parent.name.split('/')[2:]), {}) | {
                        key: {'array': f[key][:], 'attrs': attrs_parser(f[key].attrs) if f[key].attrs else None}}
                else:
                    h5dict['/'.join(f[key].parent.name.split('/')[2:])] = h5dict.setdefault('/'.join(f[key].parent.name.split('/')[2:]), {}) | {key: {
                        'shape': f[key].shape, 'attrs': attrs_parser(f[key].attrs) if f[key].attrs else None}}
            return h5dict

    def attrs_parser(attrs):
        return {k: literal_eval(v) if isinstance(v, str) and '{' in v else v for k, v in attrs.items()}

    with h5.File(file_path, 'r') as f:
        return h5dump(f)


def main():
    path = "data\\encino\\h5_files\\small_default_raw_psnr_nocompress.h5"
    #dvh5file = dvh5_reader(path, full_load=True)
    dvh5file = dvh5(path)
    print(dvh5file)


if __name__ == '__main__':
    main()
